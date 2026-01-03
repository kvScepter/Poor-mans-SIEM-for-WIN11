import win32api

def get_file_info(file_path):
    """Lukee Windows-tiedoston kuvauksen ja valmistajan."""
    if not file_path: return "Tuntematon", "Tuntematon"
    try:
        # Haetaan kielitiedot
        lang, codepage = win32api.GetFileVersionInfo(file_path, '\\VarFileInfo\\Translation')[0]
        str_info = u'\\StringFileInfo\\%04X%04X\\%s'
        
        # Haetaan kuvaus ja yritys
        desc = win32api.GetFileVersionInfo(file_path, str_info % (lang, codepage, "FileDescription"))
        comp = win32api.GetFileVersionInfo(file_path, str_info % (lang, codepage, "CompanyName"))
        
        return desc.strip(), comp.strip()
    except:
        return "Ei kuvausta", "Ei valmistajaa"
