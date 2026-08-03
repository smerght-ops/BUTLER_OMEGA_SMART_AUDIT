import fitz

doc = fitz.open("A_99_TEST_DATA/hello.pdf")

page = doc.load_page(0)

pix = page.get_pixmap()

pix.save("A_99_TEST_DATA/hello_render.png")

print("SUCCESS")