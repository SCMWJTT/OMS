// ONE API: comments and suggested edits for the ONE portal, stored in Cloudflare D1.
// Anyone may read and write (demo). Staff sign-in comes later.
const CORS = { "access-control-allow-origin": "*", "access-control-allow-methods": "GET, POST, OPTIONS", "access-control-allow-headers": "content-type" };
const json = (data, status = 200) => new Response(JSON.stringify(data), { status, headers: { "content-type": "application/json", ...CORS } });
const bad = (msg, status = 400) => json({ error: msg }, status);
const DOC = /^ACE-[A-Z]{3}-[A-Z]{3}-\d{3}(-[A-Z]{3})?$/;
const STATUS = new Set(["open", "accepted", "rejected", "resolved"]);
const clip = (s, n) => String(s ?? "").slice(0, n);
const now = () => new Date().toISOString();
const newId = () => crypto.randomUUID().replace(/-/g, "").slice(0, 12);

const shape = (r, replies) => ({ id: r.id, doc: r.doc, rev: r.rev, bm: r.bm, pidx: r.pidx, quote: r.quote, kind: r.kind, body: r.body, newText: r.new_text, author: r.author,
  created: r.created, status: r.status, statusBy: r.status_by, statusAt: r.status_at, replies: replies.filter((x) => x.note_id === r.id).map((x) => ({ author: x.author, body: x.body, created: x.created })) });

async function list(env, doc) {
  const notes = doc ? await env.DB.prepare("SELECT * FROM notes WHERE doc = ? ORDER BY created").bind(doc).all() : await env.DB.prepare("SELECT * FROM notes ORDER BY created").all();
  const ids = notes.results.map((n) => n.id);
  const replies = ids.length ? (await env.DB.prepare(`SELECT * FROM replies WHERE note_id IN (${ids.map(() => "?").join(",")}) ORDER BY created`).bind(...ids).all()).results : [];
  return notes.results.map((n) => shape(n, replies));
}
async function one(env, id) { const n = await env.DB.prepare("SELECT * FROM notes WHERE id = ?").bind(id).first(); if (!n) return null; const r = (await env.DB.prepare("SELECT * FROM replies WHERE note_id = ? ORDER BY created").bind(id).all()).results; return shape(n, r); }

export default {
  async fetch(req, env) {
    if (req.method === "OPTIONS") return new Response(null, { headers: CORS });
    const url = new URL(req.url); const p = url.pathname.replace(/\/+$/, "");
    try {
      if (req.method === "GET" && (p === "" || p === "/health")) return json({ ok: true, service: "ONE API" });
      if (req.method === "GET" && p === "/notes") { const doc = url.searchParams.get("doc"); if (doc && !DOC.test(doc)) return bad("Unknown document number"); return json(await list(env, doc)); }
      if (req.method === "POST" && p === "/notes") {
        const b = await req.json();
        if (!DOC.test(b.doc || "")) return bad("Unknown document number");
        if (!["comment", "suggestion"].includes(b.kind)) return bad("Kind must be comment or suggestion");
        if (b.kind === "comment" && !String(b.body || "").trim()) return bad("A comment needs text");
        if (b.kind === "suggestion" && !String(b.newText || "").trim()) return bad("A suggested edit needs the new wording");
        const id = newId(), t = now();
        await env.DB.prepare("INSERT INTO notes (id, doc, rev, bm, pidx, quote, kind, body, new_text, author, created, status) VALUES (?,?,?,?,?,?,?,?,?,?,?, 'open')")
          .bind(id, b.doc, clip(b.rev, 10), clip(b.bm, 80), Number(b.pidx) | 0, clip(b.quote, 8000), b.kind, clip(b.body, 4000), clip(b.newText, 8000), clip(b.author || "Anonymous", 80), t).run();
        return json(await one(env, id), 201);
      }
      let m = p.match(/^\/notes\/([a-zA-Z0-9]+)\/reply$/);
      if (req.method === "POST" && m) { const b = await req.json(); if (!String(b.body || "").trim()) return bad("A reply needs text"); if (!(await one(env, m[1]))) return bad("Not found", 404);
        await env.DB.prepare("INSERT INTO replies (id, note_id, author, body, created) VALUES (?,?,?,?,?)").bind(newId(), m[1], clip(b.author || "Anonymous", 80), clip(b.body, 4000), now()).run();
        return json(await one(env, m[1])); }
      m = p.match(/^\/notes\/([a-zA-Z0-9]+)\/status$/);
      if (req.method === "POST" && m) { const b = await req.json(); if (!STATUS.has(b.status)) return bad("Unknown status"); if (!(await one(env, m[1]))) return bad("Not found", 404);
        await env.DB.prepare("UPDATE notes SET status = ?, status_by = ?, status_at = ? WHERE id = ?").bind(b.status, clip(b.by || "Document owner", 80), now(), m[1]).run();
        return json(await one(env, m[1])); }
      return bad("Not found", 404);
    } catch (e) { return bad("Server error: " + (e.message || e), 500); }
  },
};
