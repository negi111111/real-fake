import datetime
import flask
import functools
import json
import random

random.seed(42)

app = flask.Flask('real/fake')
app.secret_key = '9)P39f.a2C99d9+wH662[=*@'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 60


def load_data(labels_file, sample_size=50):
    labels_map = json.load(open('labels.json'))
    items = list(labels_map.items())
    real_items = [item for item in items if item[1]]
    fake_items = [item for item in items if not item[1]]
    random.shuffle(real_items)
    random.shuffle(fake_items)
    real_items = real_items[:sample_size]
    fake_items = fake_items[:sample_size]
    assert len(real_items) == len(fake_items), (len(real_items),
                                                len(fake_items))

    return zip(*real_items, *fake_items)


IMAGES, LABELS = load_data('labels.json')


def nocache(view):
    @functools.wraps(view)
    def no_cache(*args, **kwargs):
        response = flask.make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.datetime.now()
        response.headers[
            'Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return functools.update_wrapper(no_cache, view)


def reset():
    flask.session['real_predictions'] = 0
    flask.session['fake_predictions'] = 0
    flask.session['real_correct'] = 0
    flask.session['fake_correct'] = 0


def get_image_url(image_index):
    return flask.url_for('static', filename=IMAGES[image_index])


@app.route('/')
@app.route('/<int:image_index>')
@nocache
def index(image_index=0):
    if image_index == 0:
        reset()
    flask.session['image_index'] = image_index
    return flask.render_template(
        'index.html',
        image_url=get_image_url(image_index),
        image_count=image_index,
        number_of_images=len(LABELS))


@app.route('/predict/', methods=['POST'])
def predict():
    prediction = flask.request.json['prediction']
    image_index = flask.session['image_index']
    if prediction is not None and image_index < len(LABELS):
        if LABELS[image_index]:
            flask.session['real_predictions'] += 1
        else:
            flask.session['fake_predictions'] += 1
        if prediction == LABELS[image_index]:
            if prediction:
                flask.session['real_correct'] += 1
            else:
                flask.session['fake_correct'] += 1
    image_index += 1
    if image_index < len(LABELS):
        new_url = flask.url_for('index', image_index=image_index)
    else:
        new_url = flask.url_for('done')
    response = json.dumps({
        'image_index': image_index,
        'prediction': prediction,
        'new_url': new_url,
    })
    print(response)
    flask.session['image_index'] = image_index
    return response, 200, {'ContentType': 'application/json'}


@app.route('/done')
def done():
    return flask.render_template(
        'done.html',
        real_correct=flask.session['real_correct'],
        fake_correct=flask.session['fake_correct'],
        real_predictions=flask.session['real_predictions'],
        fake_predictions=flask.session['fake_predictions'])


def main():
    app.run('0.0.0.0', debug=True)


if __name__ == '__main__':
    main()
