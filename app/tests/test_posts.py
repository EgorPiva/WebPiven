from datetime import datetime


def test_posts_index_status(client):
    response = client.get("/posts")
    assert response.status_code == 200


def test_posts_index_template(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch(
            "app.app.posts_list",
            return_value=posts_list,
            autospec=True
        )

        _ = client.get('/posts')
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'posts.html'
        assert context['title'] == 'Посты'
        assert len(context['posts']) == 1


def test_posts_index_context_has_posts(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch(
            "app.app.posts_list",
            return_value=posts_list,
            autospec=True
        )

        _ = client.get('/posts')
        _, context = templates[0]
        assert 'posts' in context
        assert context['posts'][0]['title'] == posts_list[0]['title']


def test_posts_index_renders_post_title(client, mocker, posts_list):
    mocker.patch("app.app.posts_list", return_value=posts_list, autospec=True)
    response = client.get("/posts")
    assert posts_list[0]['title'] in response.text


def test_posts_index_renders_post_author(client, mocker, posts_list):
    mocker.patch("app.app.posts_list", return_value=posts_list, autospec=True)
    response = client.get("/posts")
    assert posts_list[0]['author'] in response.text


def test_posts_index_renders_post_date_format(client, mocker, posts_list):
    mocker.patch("app.app.posts_list", return_value=posts_list, autospec=True)
    response = client.get("/posts")
    assert posts_list[0]['date'].strftime('%d.%m.%Y') in response.text


def test_post_page_status(client, mocker, posts_list):
    mocker.patch("app.app.posts_list", return_value=posts_list, autospec=True)
    response = client.get("/posts/0")
    assert response.status_code == 200


def test_post_page_template(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch(
            "app.app.posts_list",
            return_value=posts_list,
            autospec=True
        )

        _ = client.get('/posts/0')
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'post.html'
        assert context['title'] == posts_list[0]['title']
        assert context['post']['title'] == posts_list[0]['title']


def test_post_page_context_contains_post(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch(
            "app.app.posts_list",
            return_value=posts_list,
            autospec=True
        )

        _ = client.get('/posts/0')
        _, context = templates[0]
        assert 'post' in context
        assert context['post']['author'] == posts_list[0]['author']


def test_post_page_renders_title(client, mocker, posts_list):
    mocker.patch("app.app.posts_list", return_value=posts_list, autospec=True)
    response = client.get("/posts/0")
    assert posts_list[0]['title'] in response.text


def test_post_page_renders_author(client, mocker, posts_list):
    mocker.patch("app.app.posts_list", return_value=posts_list, autospec=True)
    response = client.get("/posts/0")
    assert posts_list[0]['author'] in response.text


def test_post_page_renders_date_format(client, mocker, posts_list):
    mocker.patch("app.app.posts_list", return_value=posts_list, autospec=True)
    response = client.get("/posts/0")
    assert posts_list[0]['date'].strftime('%d.%m.%Y') in response.text


def test_post_page_renders_image(client, mocker, posts_list):
    mocker.patch("app.app.posts_list", return_value=posts_list, autospec=True)
    response = client.get("/posts/0")
    assert f"/static/images/{posts_list[0]['image_id']}" in response.text


def test_post_page_renders_text(client, mocker, posts_list):
    mocker.patch("app.app.posts_list", return_value=posts_list, autospec=True)
    response = client.get("/posts/0")
    assert posts_list[0]['text'] in response.text


def test_post_page_has_comment_form(client, mocker, posts_list):
    mocker.patch("app.app.posts_list", return_value=posts_list, autospec=True)
    response = client.get("/posts/0")
    assert "Оставьте комментарий" in response.text
    assert "Отправить" in response.text


def test_post_page_renders_comments_and_replies(client, mocker):
    post = {
        'title': 'Р—Р°РіРѕР»РѕРІРѕРє РїРѕСЃС‚Р°',
        'text': 'РўРµРєСЃС‚ РїРѕСЃС‚Р°',
        'author': 'РРІР°РЅРѕРІ РРІР°РЅ РРІР°РЅРѕРІРёС‡',
        'date': datetime(2025, 3, 10),
        'image_id': '123.jpg',
        'comments': [
            {
                'author': 'Comment Author',
                'text': 'Comment text',
                'replies': [
                    {
                        'author': 'Reply Author',
                        'text': 'Reply text'
                    }
                ]
            }
        ]
    }
    mocker.patch("app.app.posts_list", return_value=[post], autospec=True)
    response = client.get("/posts/0")
    assert "Comment Author" in response.text
    assert "Comment text" in response.text
    assert "Reply Author" in response.text
    assert "Reply text" in response.text


def test_post_page_404_for_missing_post(client, mocker, posts_list):
    mocker.patch("app.app.posts_list", return_value=posts_list, autospec=True)
    response = client.get("/posts/999")
    assert response.status_code == 404
