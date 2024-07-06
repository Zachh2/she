from flask import Flask, request, jsonify
import requests
import re
import json
import random
import uuid

app = Flask(__name__)

@app.route('/create_page', methods=['GET'])
def create_page():
    try:
        name = request.args.get('name')
        category = request.args.getlist('category')
        token = request.args.get('token')

        r = requests.Session()
        vir = {
            "params": {
                "client_input_params": {
                    "cp_upsell_declined": 0,
                    "category_ids": category,
                    "profile_plus_id": "0",
                    "page_id": "0"
                },
                "server_params": {
                    "name": name,
                    "INTERNAL__latency_qpl_instance_id": random.randrange(36700000, 36800000),
                    "creation_source": "android",
                    "screen": "category",
                    "referrer": "pages_tab_launch_point",
                    "INTERNAL__latency_qpl_marker_id": float(str('{:.13f}'.format(random.random() + 3)) + 'E13'),
                    "variant": 5
                }
            }
        }
        var = {
            "params": {
                "params": json.dumps(vir),
                "bloks_versioning_id": 'c3cc18230235472b54176a5922f9b91d291342c3a276e2644dbdb9760b96deec',
                "app_id": "com.bloks.www.additional.profile.plus.creation.action.category.submit"
            },
            "scale": "1",
            "nt_context": {
                "styles_id": 'e6c6f61b7a86cdf3fa2eaaffa982fbd1',
                "using_white_navbar": True,
                "pixel_ratio": 1,
                "is_push_on": True,
                "bloks_version": 'c3cc18230235472b54176a5922f9b91d291342c3a276e2644dbdb9760b96deec'
            }
        }
        payload = {
            'access_token': token,
            'method': 'post',
            'pretty': False,
            'format': 'json',
            'server_timestamps': True,
            'locale': 'id_ID',
            'purpose': 'fetch',
            'fb_api_req_friendly_name': 'FbBloksActionRootQuery-com.bloks.www.additional.profile.plus.creation.action.category.submit',
            'fb_api_caller_class': 'graphservice',
            'client_doc_id': '11994080423068421059028841356',
            'variables': json.dumps(var),
            'fb_api_analytics_tags': ["GraphServices"],
            'client_trace_id': str(uuid.uuid4())
        }
        
        pos = r.post('https://graph.facebook.com/graphql', data=payload).text.replace('\\', '')
        
        if ('profile_plus_id' in str(pos)) and ('page_id' in str(pos)):
            name, page_id, profile_id = re.findall(r'"android", "pages_tab_launch_point", "(.*?)", "(.*?)", "(.*?)", "intent_selection"', str(pos))[0]
            return jsonify({
                'status': 'Success',
                'Page Name': name,
                'Page ID': page_id,
                'Profile ID': profile_id
            })
        else:
            return jsonify({'status': 'Failed to Create Page!'})
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
