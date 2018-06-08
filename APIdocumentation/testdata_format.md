* testdata format example
    ```json
    {
        "result":{
                "0": true,
                "1": true,
                "2": true,
                ...
        },
        "skip_list":[
                {
                    "skip_vas_index": 16,
                    "suppose_vas_index": 1
                },
                {
                    "skip_vas_index": 26,
                    "suppose_vas_index": 1
                }
        ],
        "vas_cog_block": {
                "0": {
                    "path_list": [
                        {
                            "point_list": [
                                {
                                    "x": 75.68263,
                                    "y": 27.821655,
                                    "t": 1527834557496
                                },
                                {
                                    "x": 75.68263,
                                    "y": 27.821655,
                                    "t": 1527834557507
                                },
                                {
                                    "x": 75.68263,
                                    "y": 27.613342,
                                    "t": 1527834557507
                                }
                            ]
                        }
                    ],
                    "vas_ques": 2
                },
                ...
        },
        "reattempt_list": [],
        "vas_block_size": {
            "width": 180,
            "height": 162
        },
        "patient_info": {
                "years_of_education": 0,
                "patient_name": "sss",
                "assessment_date": "01/06/2018 00:00:00",
                "date_of_birth_calendar": 315505800000,
                "gender": "male",
                "setting_of_assessment": "ward",
                "patient_id": "3",
                "onset_of_stroke_calendar": 1519142400000,
                "ethnicity": "chinese",
                "onset_of_stroke": "21/02/2018 00:00:00",
                "assessment_date_calendar": 1527834420055,
                "date_of_birth": "01/01/1980 00:00:00",
                "dominant_hand": "right",
                "nihss": 0,
                "mrs": 0
        },
        "vct_raw": "[base64 encoded string]"
  }
    ```