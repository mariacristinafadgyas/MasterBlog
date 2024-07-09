import json


def read_data(file_path):
    with open(file_path, 'r') as fileobj:
        blog_data = json.load(fileobj)
        return blog_data


def sync_data(file_path, blog_data):
    updated_blog = json.dumps(blog_data)
    with open(file_path, 'w') as fileobj:
        fileobj.write(updated_blog)


def main():
    blog_data = read_data('blog_data.json')
    new_data = {
        "id": 3,
        "author": "Jane Done",
        "title": "Third Post",
        "content": "This is the new post"
    }
    blog_data.append(new_data)
    sync_data('blog_data.json', blog_data)


if __name__ == "__main__":
    main()