def add_custom_props(src, dst, props):
    zin = zipfile.ZipFile(src); zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
    items = "".join(f'<property fmtid="{{D5CDD505-2E9C-101B-9397-08002B2CF9AE}}" pid="{i+2}" name="{k}"><vt:lpwstr>{v.replace("&","&amp;")}</vt:lpwstr></property>' for i,(k,v) in enumerate(props.items()))
    custom = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/custom-properties" '
              'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">' + items + '</Properties>')
    for it in zin.infolist():
        data = zin.read(it.filename)
        if it.filename == "[Content_Types].xml" and b"custom-properties" not in data:
            data = data.replace(b"</Types>", b'<Override PartName="/docProps/custom.xml" ContentType="application/vnd.openxmlformats-officedocument.custom-properties+xml"/></Types>')
        if it.filename == "_rels/.rels" and b"custom-properties" not in data:
            data = data.replace(b"</Relationships>", b'<Relationship Id="rIdCustom1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/custom-properties" Target="docProps/custom.xml"/></Relationships>')
        if it.filename != "docProps/custom.xml": zout.writestr(it, data)
    zout.writestr("docProps/custom.xml", custom); zout.close(); zin.close()
