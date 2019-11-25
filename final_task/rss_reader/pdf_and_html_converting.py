import urllib
from fpdf import FPDF
import os
import shutil
from pathlib import Path


def drawing_image(file_name):
    from PIL import Image
    from PIL import ImageFont
    from PIL import ImageDraw

    img = Image.new("RGB", (480, 360))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial', 60)
    draw.text((120, 120), "No image", (255, 255, 255), font=font)
    img.save('{0}'.format(file_name))


def checking_path():
    return "Imag\\"


def getting_images(path, pack_of_news):
    deleting_images(path)
    symbol = ':'
    try:
        os.mkdir(os.path.abspath(path.joinpath(Path(checking_path()))))
    except OSError:
        print("Creating directory %s hasn't been complete!" % path)
    for item in pack_of_news:
        name_by_date = item.time_of_novelty.replace(symbol, '')
        url = item.images_links
        file_name = path.joinpath(Path(checking_path()).joinpath(Path(name_by_date + '.jpg')))
        try:
            img = urllib.request.urlopen(url).read()
            out = open(file_name, "wb")
            out.write(img)
            out.close()
        except FileNotFoundError:
            print("Wrong path for images.")
            break
        except ValueError:
            drawing_image(file_name)
        except TypeError:
            drawing_image(file_name)
        except urllib.error.URLError:
            drawing_image(file_name)


def deleting_images(path):
    directory = checking_path()
    try:
        shutil.rmtree(path.joinpath(Path(directory)))
    except OSError:
        print("Nothing to delete.")


def converting_to_pdf(path, pack_of_news):
    symbol = ':'
    pdf = FPDF()
    pdf.add_font('DejaVuSans', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font("DejaVuSans")
    pdf.add_page()
    if not os.path.exists(path):
        os.makedirs(path)
    getting_images(path, pack_of_news)
    for item in pack_of_news:
        name_by_date = item.time_of_novelty.replace(symbol, '')
        directory = checking_path()
        file_name = path.joinpath(Path(directory + name_by_date + '.jpg'))

        pdf.set_text_color(0, 0, 0)
        pdf.write(10, str(item.number_of_novelty) + ". " + item.title_of_novelty + "\n")
        try:
            pdf.image(str(file_name), w=140, h=100)
        except RuntimeError:
            pdf.write("NO IMAGE, BUT LINK: " + item.images_links + "\n")
        pdf.write(5, "ALT TEXT: " + item.alt_text + "\n")
        pdf.write(10, "PUBLISHED: " + item.time_of_novelty + "\n")
        pdf.write(7, "SOURCE LINK: " + item.source_link + "\n\n")
        pdf.set_text_color(0, 0, 255)
        pdf.write(6, "DESCRIPTION: " + item.description + "\n")
        pdf.set_text_color(0, 0, 0)
        pdf.write(7, "\nIMAGES LINKS: " + item.images_links + "\n")
        pdf.write(6, "MAIN SOURCE LINK: " + item.main_source + "\n")
    try:
        pdf.output((path.joinpath(Path('News.pdf'))))  # Create pdf in path
    except PermissionError:
        print("Something wrong with your path in pdf!")
    except FileNotFoundError:
        print("You entered wrong path!")


def converting_to_html(path, pack_of_news):
    symbol = ':'
    if not os.path.exists(path):
        os.makedirs(path)
    getting_images(path, pack_of_news)
    path_to_file = path.joinpath(Path("Html_news.html"))
    try:
        with open(path_to_file, 'w', encoding='utf-8') as html_news:
            for item in pack_of_news:
                name_by_date = item.time_of_novelty.replace(symbol, '')
                directory = checking_path()
                file_name = path.joinpath(Path(directory + name_by_date + '.jpg'))
                html_news.write(f"<p>{item.number_of_novelty}.<br> <strong>Title: {item.title_of_novelty}</strong><br>")
                html_news.write("<span>Date: {0} </span><br> Link: <a href="">{1}</a><br>".format(item.time_of_novelty,
                                                                                                  item.source_link))
                html_news.write(f"<strong>Description</strong>:<br>{item.description}<br>")
                try:
                    html_news.write(f"Image: <br><img src='{file_name}' title='{item.alt_text}'>")
                    html_news.write("<br>Image links: <a href="">{0}</a> <br>Alternative text: {1}<br>".
                                    format(item.images_links,
                                           item.alt_text))
                except RuntimeError:
                    html_news.write(f"Image links: {item.images_links}<br> Alternative text: {item.alt_text}<br>")
                html_news.write("Main source: <a href="">{0}</a> <br></p>".format(item.main_source))
    except PermissionError:
        print("Something wrong with your path in html!")
    except FileNotFoundError:
        print("Wrong path for html.")


def html_path(list_of_args):
    try:
        return Path(list_of_args[list_of_args.index('--to-html') + 1])
    except IndexError:
        return Path(os.curdir)


def pdf_path(list_of_args):
    try:
        return Path(list_of_args[list_of_args.index('--to-pdf') + 1])
    except IndexError:
        return Path(os.curdir)
