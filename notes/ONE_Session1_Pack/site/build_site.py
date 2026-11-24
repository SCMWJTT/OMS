# Builds ONE_Library.html from site.tpl + index.json
t = open("/home/claude/site/site.tpl").read()
d = open("/home/claude/site/index.json").read().replace("</", "<\\/")
open("/home/claude/site/ONE_Library.html", "w").write(t.replace("__DATA__", d))
print("ONE_Library.html written")
