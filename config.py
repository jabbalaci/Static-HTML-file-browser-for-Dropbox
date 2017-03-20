# CONFIGURATION FILE of Static HTML file browser for Dropbox

# this is a link to the icons directory
# DROPBOX_BASE_URL = "https://dl.dropboxusercontent.com/u/144888"

GITHUB_IO_BASE_URL = "https://jabbalaci.github.io/teaching-assets"
DROPBOX_LINK_TO_ICONS = "{base}/icons".format(base=GITHUB_IO_BASE_URL)

# here you can change the output of the program
SHOW_SERVER_INFO = True         # default: True
HIDE_HIDDEN_ENTRIES = True      # default: True
HIDE_INDEX_HTML_FILES = True    # default: True
HIDE_ICONS_FOLDER = True        # default: True
MONOSPACED_FONTS = True         # default: True
SERVER_INFO = "Apache/2.4.23 at github.io Port 80"

# icons folder in your dropbox
# DROPBOX_ICON_FOLDER = "/home/jabba/Dropbox/assets/static_html_icons"

# if you want to add more icons, you can do it here, but don't forget to
# add the gif file to the icons directory too.
extensions = {
   '.bmp': 'image2.gif',
   '.doc': 'doc.gif',
   '.flac': 'sound2.gif',
   '.gif': 'image2.gif',
   '.htm': 'link.gif',
   '.html': 'link.gif',
   '.jpeg': 'image2.gif',
   '.jpg': 'image2.gif',
   '.midi': 'sound2.gif',
   '.mp3': 'sound2.gif',
   '.mp4': 'sound2.gif',
   '.png': 'image2.gif',
   '.py': 'python.gif',
   '.tar': 'tar.gif',
   '.tex': 'tex.gif',
   '.txt': 'text.gif',
   '.wav': 'sound2.gif',
   '.wma': 'sound2.gif',
}
