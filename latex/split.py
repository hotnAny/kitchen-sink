from pypdf import PdfWriter, PdfReader

# TODO: check this
input_pdf_filename = "main.pdf"

# TODO: edit this
split_pages = [
    # ["sub_file_name", start_page, end_page]
    ["project_summary", 1, 1],
    ["project_description", 2, 16],
    ["references", 17, 21],
    ["resources", 22, 23],
    ["data", 24, 25]
]
 
# NOTE shouldn't have changed anything below
input_pdf = PdfReader(open(input_pdf_filename, "rb"), strict=False)

cnt = 0
for sp in split_pages:
    output = PdfWriter()
    for i in range(sp[1]-1, sp[2]):
        output.add_page(input_pdf.pages[i])
    pdf_out = str(cnt) + '_' + sp[0] + ".pdf"
    with open(pdf_out, "wb") as output_stream:
        output.write(output_stream)
    print(pdf_out)
    cnt+=1