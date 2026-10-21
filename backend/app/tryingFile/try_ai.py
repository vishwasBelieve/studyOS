import pymupdf

# Open the PDF document
doc = pymupdf.open("/mnt/hdd/Projects/StudyOS/backend/uploads/ai.pdf")

# Get the first page (0-indexed)
page = doc[0]

# Get a list of all images referenced on this page
image_list = page.get_images(full=True)

if image_list:
    # Get the first image's metadata (first item in the list)
    first_image = image_list[0]
    xref = first_image[0]  # The XREF is the unique ID for the image object
    
    # Extract the raw image bytes and metadata
    base_image = doc.extract_image(xref)
    image_bytes = base_image["image"]
    image_ext = base_image["ext"]  # e.g., 'png', 'jpeg'
    
    # Save the image to your disk
    with open(f"extracted_first_image.{image_ext}", "wb") as f:
        f.write(image_bytes)
    print(f"Successfully extracted the first image as 'extracted_first_image.{image_ext}'")
else:
    print("No embedded images found on the first page.")
