normal_result = ['Feed: Yahoo News - Latest News & Headlines\n', '', '\nTitle: item_title', '\nDate: item_date', '\nLink: item_link\n', 'Description: item_description\n', 'Links:\n[1]: item_link(link)', '\n[2]: media_link_url\n']


json_result = '{"Title: ": "item_title", "Date: ": "item_date", "Link: ": "item_link", "Description: ": "item_description", "Media link: ": "media_link_url"}'


html_result = '''<!DOCTYPE html>
<html>
  <head>
    <title>HTML document</title>
  </head>
  <body>
    <div>
      <h2>Title: item_title</h2>
      <p>Link: item_link</p>
      <img src="media_link_url">
      <p>Description: item_description</p>
    </div>
  </body>
</html>'''


html_result_from_db = '''<!DOCTYPE html>
<html>
  <head>
    <title>HTML document</title>
  </head>
  <body>
    <div>
      <h2>Title: item_title</h2>
      <p>Link: item_link</p>
      <p>Description: item_description</p>
    </div>
  </body>
</html>'''
