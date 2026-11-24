final = f"{OUT}/ACE-OMS-MAN-001_OMS_Manual_Rev04.docx"
add_custom_props(tmp, final + ".tmp", META); os.remove(tmp)
zin = zipfile.ZipFile(final + ".tmp"); zout = zipfile.ZipFile(final, "w", zipfile.ZIP_DEFLATED)
for it in zin.infolist():
    data = zin.read(it.filename)
    if it.filename == "docProps/app.xml":
        s = data.decode()
        s = s.replace("<Manager/>", "<Manager>Satesh Sankar — Chief Executive Officer</Manager>").replace("<Company/>", "<Company>Acme Caribbean Energy Limited</Company>")
        s = s.replace("<HyperlinkBase/>", "<HyperlinkBase>https://oms.cynmark.app/</HyperlinkBase>")
        data = s.encode()
    zout.writestr(it, data)
zout.close(); zin.close(); os.remove(final + ".tmp")
open("/home/claude/oms/out/image_placeholders.txt", "w").write("\n".join(f"{i}\t{b}" for i, b in PLACEHOLDERS))
print("saved", final, len(PLACEHOLDERS), "image placeholders")
