# coding: utf-8
import re
import urllib2

fixture_file_layout = """
var images = [
%(content)s
];

for (var i=0; i < images.length; i++) {
    db.userImages.insert(images[i]);
}
"""

mongodb_image_struct = """
{
    owner: {
        username: "rafaelcaricio"
    },
    originalUrl: "%(original_url)s"
}
"""

class IHateFlashImages(object):
    i_hate_flash_base_url = "http://ihateflash.net/set/"

    def __init__(self, party_slug):
        self.party_slug = party_slug

    def parse_all_urls(self, content):
        for line in content.readlines():
            thumb_url = re.search("http\://ihateflash.net/wp-content/uploads/\d+/\d+/[^-]+\-190x190.jpg", line)
            if thumb_url:
                yield self.to_original_url(thumb_url.group())

    def to_original_url(self, thumb_url):
        return thumb_url.replace("-190x190", "")

    def get_all_images(self):
        response = urllib2.urlopen("%s%s" % (self.i_hate_flash_base_url, self.party_slug))
        for image_url in self.parse_all_urls(response):
            yield image_url

class ImageDupper(object):

    def __init__(self, sources):
        self.sources = sources

    def gen_item(self, image_url):
        return mongodb_image_struct % {"original_url": image_url}

    def content(self):
        content_buffer = []
        for image_source in self.sources:
            for image in image_source.get_all_images():
                content_buffer.append(self.gen_item(image))
        return fixture_file_layout % {"content": ",\n".join(content_buffer)}

    def write_to_file(self, filename):
        fileout = file(filename, "w")
        fileout.write(self.content())
        fileout.flush()
        return fileout.close()


if __name__ == '__main__':
    dupper = ImageDupper([
        IHateFlashImages("vip-30-anos"),
        IHateFlashImages("fashion-rio-espaco-fashion"),
        IHateFlashImages("house-of-models-coca-cola-clothing-party")
    ])
    dupper.write_to_file("fixtures.js")

