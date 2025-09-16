import streamlit as st
import pdfkit
import os

# --------------------------
# Page Config
# --------------------------
st.set_page_config(page_title="AffiDesk - हिंदी हलफनामा जनरेटर", layout="centered")
st.title("📄 AffiDesk - Hindi Affidavit Generator")

# --------------------------
# wkhtmltopdf Path
# --------------------------
path_wkhtmltopdf = os.getenv("WKHTMLTOPDF_PATH", "/usr/local/bin/wkhtmltopdf")
if not os.path.exists(path_wkhtmltopdf):
    st.error(f"⚠️ wkhtmltopdf not found at: {path_wkhtmltopdf}")
    st.stop()
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# --------------------------
# HTML Template with Noto Sans Devanagari
# --------------------------
template_text = """
<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="UTF-8">
<style>
@font-face {
  font-family: 'Noto Sans Devanagari';
  src: url('fonts/NotoSansDevanagari-Regular.ttf') format('truetype');
}
body {
  font-family: 'Noto Sans Devanagari', sans-serif;
  margin: 30px;
  line-height: 1.6;
}
h2 { text-align: center; margin-bottom: 20px; }
table { width: 100%; border-collapse: collapse; }
th, td { border: 1px solid #000; padding: 6px; text-align: center; }
th { background-color: #eee; }
.heirs-table { overflow-x: auto; }
.sapathkarta { text-align: right; margin-right: 50px; margin-top: 20px; }
</style>
</head>
<body>

<div style="height:100px;"></div>
<h2>हलफनामा</h2>

<p>मनकि {name} {son_or_daughter} {father_name} निवासी मकान न० {house_no} {village_name} 
तहसील {tehsil} जिला {district} हरियाणा का / की हूँ | जोकि मैं निम्नलिखित हलफन ब्यान 
करते / करता हूँ |</p>  

[[POINTS_HERE]]

<div class="sapathkarta">
    <p>सपथकर्ता</p>
</div>

<p><b>तसदीक-</b><br>
तसदीक की जाती है कि उपरोक्त ब्यान हमारे ज्ञान व इल्म के अनुसार सही एवं दुरुस्त है  
तथा इसमें हमने कुछ छुपाया नहीं है |</p>

<div class="sapathkarta">
    <p>सपथकर्ता</p>
</div>

</body>
</html>
"""

# --------------------------
# Input Form
# --------------------------
with st.form("affidavit_form"):
    name = st.text_input("नाम")
    son_or_daughter = st.selectbox("संबंध", ["पुत्र", "पुत्री"])
    father_name = st.text_input("पिता का नाम")
    grandfather_name = st.text_input("दादा का नाम")
    house_no = st.text_input("मकान नं")
    village_name = st.text_input("गाँव का नाम")
    tehsil = st.text_input("तहसील")
    district = st.text_input("जिला")
    death_certificate_number = st.text_input("मृत्यु रजिस्ट्रेशन संख्या")
    date_of_death = st.date_input("मृत्यु की तिथि")
    transfer_deed_number = st.text_input("ट्रांसफर डीड संख्या")
    date_of_transfer_deed = st.date_input("ट्रांसफर डीड दिनांक")
    no_of_sons = st.text_input("पुत्रों की संख्या (हिन्दी में जैसे - एक, दो, तीन आदि)")
    khewat_number = st.text_input("खेवट संख्या")

    include_point5 = st.checkbox(
        "अगर किसी खेवट से स्टे हटी है, वो पॉइंट भी दिखाना चाहते हो तो ये विकल्प चुने",
        value=True
    )

    heirs_count = st.number_input("वारिसों की संख्या", min_value=1, max_value=20, step=1)
    heirs = []
    for i in range(int(heirs_count)):
        hname = st.text_input(f"वारिस {i+1} का नाम", key=f"hname_{i}")
        hrel = st.text_input(f"वारिस {i+1} का मृतक से संबंध", key=f"hrel_{i}")
        heirs.append((hname, hrel))

    submitted = st.form_submit_button("हलफनामा बनाएँ")

# --------------------------
# Generate PDF
# --------------------------
if submitted:
    heirs_html = '<div class="heirs-table"><table><tr><th>क्रम सं.</th><th>वारिस का नाम</th><th>मृतक से संबंध</th></tr>'
    for i, (hname, hrel) in enumerate(heirs, start=1):
        heirs_html += f"<tr><td>{i}</td><td>{hname}</td><td>{hrel}</td></tr>"
    heirs_html += "</table></div>"

    points = []
    points.append(f"यह है कि मेरे पिताजी {father_name} पुत्र {grandfather_name} का मृत्यु रजिस्ट्रेशन न० {death_certificate_number} देहांत {date_of_death} को हो चुकी थी |")
    points.append(f"यह है कि मेरे पिताजी {father_name} पुत्र {grandfather_name} के हम निम्नलिखित वारिसान हैं :<br>{heirs_html}")
    points.append(f"यह है कि उपरोक्त वारसान के इलावा मेरे पिताजी {father_name} पुत्र {grandfather_name} की जायदाद की संपत्ति के अन्य कोई वारसान नहीं है |")
    points.append(f"यह है कि मेरे पिताजी {father_name} पुत्र {grandfather_name} ने मरने से पहले एक ट्रांसफर डीड वासिका न० {transfer_deed_number} दिनांक {date_of_transfer_deed} को तहसील {tehsil} {district} हरियाणा में अपने {no_of_sons} के हक में कर दी थी |")
    if include_point5:
        points.append(f"यह है कि गाँव {village_name} में खेवट न० {khewat_number} में पहले स्टे था लेकिन अब वह स्टे हट गई है |")
    points.append("यह है कि विरासत का इंतक़ाल राजस्व विभाग में उपरोक्त नामों पर दर्ज किया जावे | मुझे किसी प्रकार का कोई उज़र व ऐतराज़ नहीं होगा |")
    points.append("यह है कि उपरोक्त वारिसान की जिम्मेवारी मेरी स्वयं की होगी |")
    points.append("यह है कि हमारे उपरोक्त लिखित कथन सत्य व दुरुस्त है |")

    points_html = "".join([f"<p>{i+1}. {p}</p>\n" for i, p in enumerate(points)])
    html_content = template_text.format(
        name=name, son_or_daughter=son_or_daughter, father_name=father_name,
        grandfather_name=grandfather_name, house_no=house_no, village_name=village_name,
        tehsil=tehsil, district=district
    ).replace("[[POINTS_HERE]]", points_html)

    output_file = "hindi_affidavit.pdf"
    pdfkit.from_string(html_content, output_file, configuration=config, options={"encoding": "UTF-8"})

    st.success("✅ हलफनामा तैयार हो गया!")
    with open(output_file, "rb") as f:
        st.download_button("⬇️ हलफनामा डाउनलोड करें (PDF)", f, file_name="hindi_affidavit.pdf")




