import os


def test_update_app():
    update_info = {'_version_num': '1.0', "_download_url": "/doo"}
    file_path = os.path.dirname(os.path.realpath(__file__)) + '/appreadme.txt'
    with open(file_path) as f:
        release_notes = f.read()
        update_info['_release_note'] = release_notes
    print()
    print(update_info['_release_note'])