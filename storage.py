import json


def read_data(file_path):
    """Reads the JSON file and returns the data. Handles errors if the file
     doesn't exist or contains invalid JSON."""
    try:
        with open(file_path, 'r') as fileobj:
            blog_data = json.load(fileobj)
            return blog_data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


def sync_data(file_path, blog_data):
    """Writes data to the JSON file. Handles errors that might occur during the write process."""
    try:
        updated_blog = json.dumps(blog_data)
        with open(file_path, 'w') as fileobj:
            fileobj.write(updated_blog)
    except IOError:
        print(f"Error: Unable to write to file {file_path}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def fetch_post_by_id(file_path, post_id):
    """Fetches the post by id"""
    blog_data = read_data(file_path)
    for post in blog_data:
        if post['id'] == post_id:
            return post
    return None


def update_post_in_json(file_path, updated_post):
    """Updates the post in the JSON file"""
    blog_data = read_data(file_path)
    for post in blog_data:
        if post['id'] == updated_post['id']:
            post['title'] = updated_post['title']
            post['author'] = updated_post['author']
            post['content'] = updated_post['content']
            post['likes'] = updated_post['likes']
            break

    sync_data('blog_data.json', blog_data)


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
    # print(fetch_post_by_id('blog_data.json', 3))


if __name__ == "__main__":
    main()