# -*- coding: utf-8 -*-
import streamlit as st
import pdfkit
import os
from datetime import datetime

# --------------------------
# Page Config
# --------------------------
st.set_page_config(
    page_title="AffiDesk - हिंदी हलफनामा जनरेटर",
    page_icon="📜",
    layout="centered"
)

# --------------------------
# Mobile-Friendly CSS
# --------------------------
st.markdown(
    """
    <style>
    body {
        font-family: 'Noto Sans Devanagari', sans-serif;
    }
    .main-title {
        text-align: center;
        color: #2C3E50;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #555;
        font-size: 1rem;
        margin-bottom: 20px;
    }
    .heirs-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
    }
    .heirs-table th, .heirs-table td {
        padding: 6px;
        text-align: center;
        border: 1px solid #ccc;
        word-wrap: break-word;
    }
    /* Make table scrollable on small screens */
    .table-container {
        overflow-x: auto;
    }
    .footer {
        text-align: center;
        color: gray;
        font-size: 12px;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------
# Branding
# --------------------------
st.markdown("<h1 class='main-title'>📜 AffiDesk</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='subtitle'>सरल और भरोसेमंद हिंदी हलफनामा जनरेटर</h4>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("ℹ️ ऐप जानकारी")
st.sidebar.write(
    "AffiDesk एक सरल और भरोसेमंद टूल है जिससे आप हिंदी में हलफनामा बना सकते हैं।\n\n"
    "✔️ डायनामिक पॉइंट्स\n"
    "✔️ वारिसों की टेबल\n"
    "✔️ सही हिंदी PDF\n\n"
    "मोबाइल और डेस्कटॉप दोनों पर काम करता है ✅"
)

# --------------------------
# Path to wkhtmltopdf
# --------------------------
path_wkhtmltopdf = "/usr/bin/wkhtmltopdf"
if not os.path.exists(path_wkhtmltopdf):
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# --------------------------
# Template HTML
# --------------------------
template_text = """
<div style="height:40px;"></div>

<h2 style="text-align:center; margin-bottom:20px;">हलफनामा</h2>

<p>मनकि {name} {son_or_daughter} {father_name} निवासी मकान न० {house_no} {village_name} 
तहसील {tehsil} जिला {district} हरियाणा का / की हूँ | जोकि मैं निम्नलिखित हलफन ब्यान 
करते / करता हूँ |</p>  

[[POINTS_HERE]]

<br><br>
<div style="text-align:right; margin-right:20px;">
    <p>सपथकर्ता</p>
</div>

<p><b>तसदीक-</b><br>
तसदीक की जाती है कि उपरोक्त ब्यान हमारे ज्ञान व इल्म के अनुसार सही एवं दुरुस्त है  
तथा इसमें हमने कुछ छुपाया नहीं है |</p>

<div style="text-align:right; margin-right:20px; margin-top:20px;">
    <p>सपथकर्ता</p>
</div>

<hr>
<p class="footer">AffiDesk © {year} | Developed with ❤️</p>
"""

# --------------------------
# Input Form
# --------------------------
with st.form("affidavit_form"):
    st.subheader("📝 विवरण दर्ज करें")

    name = st.text_input("नाम")
    son_or_daughter = st.selectbox("संबंध", ["पुत्र", "पुत्री"])
    father_name = st.text_input("पिता का नाम")
    grandfather_name = st.text_input("दादा का नाम")
    house_no = st.text_input("मकान नं")
    village_name = st.text_input("गाँव का नाम")
    tehsil = st.text_input("तहसील")
    district = st.text_input("जिला")
    death_certificate_number = st.text_input("मृत्यु रजिस्ट्रेशन संख्या")
    date_of_death = st.text_input("मृत्यु की तिथि (DD-MM-YYYY)")
    transfer_deed_number = st.text_input("ट्रांसफर डीड संख्या")
    date_of_transfer_deed = st.text_input("ट्रांसफर डीड दिनांक (DD-MM-YYYY)")
    no_of_sons = st.text_input("पुत्रों की संख्या")
    khewat_number = st.text_input("खेवट संख्या")

    include_point5 = st.checkbox("👉 अगर किसी खेवट से स्टे हटी है तो यह पॉइंट शामिल करें", value=True)

    heirs_count = st.number_input("वारिसों की संख्या", min_value=1, max_value=20, step=1)
    heirs = []
    for i in range(int(heirs_count)):
        hname = st.text_input(f"वारिस {i+1} का नाम", key=f"hname_{i}")
        hrel = st.text_input(f"वारिस {i+1} का मृतक से संबंध", key=f"hrel_{i}")
        heirs.append((hname, hrel))

    submitted = st.form_submit_button("📄 हलफनामा बनाएँ")

# --------------------------
# Generate PDF
# --------------------------
if submitted:
    # Table
    heirs_html = """
    <div class="table-container">
    <table class="heirs-table">
        <tr>
            <th>क्रम सं.</th>
            <th>वारसान का नाम</th>
            <th>मृतक से संबंध</th>
        </tr>
    """
    for i, (hname, hrel) in enumerate(heirs, start=1):
        heirs_html += f"<tr><td>{i}</td><td>{hname}</td><td>{hrel}</td></tr>"
    heirs_html += "</table></div>"

    # Points
    points = []
    points.append(
        f"यह है कि मेरे पिताजी {father_name} पुत्र {grandfather_name} का मृत्यु "
        f"रजिस्ट्रेशन न० {death_certificate_number} देहांत {date_of_death} को हो चुकी थी |"
    )
    points.append(
        f"यह है कि मेरे पिताजी {father_name} पुत्र {grandfather_name} के हम निम्नलिखित वारिसान हैं :<br>{heirs_html}"
    )
    points.append(
        f"यह है कि उपरोक्त वारसान के इलावा मेरे पिताजी {father_name} पुत्र {grandfather_name} "
        f"की जायदाद की संपत्ति के अन्य कोई वारसान नहीं है |"
    )
    points.append(
        f"यह है कि मेरे पिताजी {father_name} पुत्र {grandfather_name} ने मरने से पहले एक "
        f"ट्रांसफर डीड वासिका न० {transfer_deed_number} दिनांक {date_of_transfer_deed} को "
        f"तहसील {tehsil} {district} हरियाणा में अपने {no_of_sons} के हक में कर दी थी |"
    )
    if include_point5:
        points.append(
            f"यह है कि गाँव {village_name} में खेवट न० {khewat_number} में पहले स्टे था लेकिन अब वह स्टे हट गई है |"
        )
    points.append(
        "यह है कि विरासत का इंतक़ाल राजस्व विभाग में उपरोक्त नामों पर दर्ज किया जावे | "
        "मुझे किसी प्रकार का कोई उज़र व ऐतराज़ नहीं होगा |"
    )
    points.append("यह है कि उपरोक्त वारिसान की जिम्मेवारी मेरी स्वयं की होगी |")
    points.append("यह है कि हमारे उपरोक्त लिखित कथन सत्य व दुरुस्त है |")

    points_html = "".join([f"<p>{i+1}. {p}</p>" for i, p in enumerate(points)])

    # Final content
    html_content = template_text.format(
        name=name, son_or_daughter=son_or_daughter, father_name=father_name,
        grandfather_name=grandfather_name, house_no=house_no, village_name=village_name,
        tehsil=tehsil, district=district, year=datetime.now().year
    ).replace("[[POINTS_HERE]]", points_html)

    output_file = f"hindi_affidavit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdfkit.from_string(html_content, output_file, configuration=config, options={"encoding": "UTF-8"})

    st.success("✅ आपका हलफनामा तैयार हो गया!")
    with open(output_file, "rb") as f:
        st.download_button("⬇️ हलफनामा डाउनलोड करें (PDF)", f, file_name="hindi_affidavit.pdf")
