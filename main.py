from flask import Flask, jsonify
import requests
from flask import request
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/test', methods=['POST'])
def hello_world():
    data = request.get_json()  # a multidict containing POST data
    print(data['test'])
    return 'hello test'


@app.route('/get_brands', methods=['POST'])
def post_brands():
    data = request.get_json()  # a multidict containing POST data
    start_date=data['start_date']
    end_date=data['end_date']
    print(start_date,end_date)
    dummy_start_date = 1608209422374
    dummy_end_date = 1639745412436
    api_url = 'https://app.socialinsider.io/api'
    create_row_data = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "socialinsider_api.get_brands",
        "params": {
            "projectname": "API_test"
        }}
    headers = {"Authorization": "Bearer API_KEY_TEST"}

    r = requests.post(url=api_url, json=create_row_data, headers=headers)
    json_data = json.loads(r.text)
    myList = []
    for result in json_data['result']:
        brand_likes = 0
        brand_fans = 0
        brand_count_profile_type = len(result['profiles'])

        print(result['brandname'])
        for names in result['profiles']:
            likes_by_profile_type, fans_by_profile_type = calculate_stats_by_profile_type(names['id'],
                                                                                          names['profile_type'],
                                                                                          start_date,
                                                                                          end_date)
            brand_likes = brand_likes + likes_by_profile_type
            brand_fans = brand_fans + fans_by_profile_type
        dict = {"BrandName": result['brandname'], "Count": brand_count_profile_type, "fans": brand_fans,
                "likes": brand_likes}
        myList.append(dict)
        print("COUNT:", brand_count_profile_type, "BRAND FANS: ", brand_fans, "BRAND LIKES: ", brand_likes)

    return jsonify(myList)
    #return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


def calculate_stats_by_profile_type(id, profile_type, start_date, end_date):
    likes_profile_type = 0
    fans_profile_type = 0
    api_url = 'https://app.socialinsider.io/api'
    body = {
        "id": 1,
        "method": "socialinsider_api.get_profile_data",
        "params": {
            "id": id,
            "profile_type": profile_type,
            "date": {
                "start": start_date,
                "end": end_date,
                "timezone": "Europe/London"
            }
        }
    }
    headers = {"Authorization": "Bearer API_KEY_TEST"}

    response = requests.post(url=api_url, json=body, headers=headers)
    json_data = json.loads(response.text)
    # print(json_data['resp'][id])
    for dates in json_data['resp'][id]:
        if 'likes' in json_data['resp'][id][dates]:
            if json_data['resp'][id][dates]['likes'] is not None:
                likes_profile_type = likes_profile_type + json_data['resp'][id][dates]['likes']
        if 'fans' in json_data['resp'][id][dates]:
            if json_data['resp'][id][dates]['fans'] is not None:
                fans_profile_type = fans_profile_type + json_data['resp'][id][dates]['fans']
    # print(likes_profile_type)
    # print(fans_profile_type)
    return likes_profile_type, fans_profile_type


if __name__ == '__main__':
    app.run()
