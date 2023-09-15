from lxml import etree

# Load the SVG file
svg_filename = "./output.svg"
tree = etree.parse(svg_filename)
root = tree.getroot()

# Find and modify specific elements by their attributes (e.g., class)
for element in root.xpath("//svg:rect[@class='measure']", namespaces={"svg": "http://www.w3.org/2000/svg"}):
    # Modify the fill color
    element.set("fill", "red")

# Save the modified SVG
tree.write("colored_output.svg", pretty_print=True)