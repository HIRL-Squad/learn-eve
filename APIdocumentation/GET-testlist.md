**GET testlist**
----
  <_Additional information about your API call. Try to use verbs that match both request type (fetching vs modifying) and plurality (one vs multiple)._>

* **URL**

  /testlist

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:** None
 
   **Optional:**
   
   `where=[dictionary]` <_this dictionary contains data filter for the document's content_>
 
   `sort=[+/-field name]`
   
   `max_results=[integer]`
   
   `timestamp=[integer]` <_This is a dummy param to avoid caching_>

* **Data Params**

    None
    
* **Success Response:**
  
  * **Code:** 200 <br />
    **Content example:** 
    ```json
    {
    "_meta": {
        "max_results": 20,
        "page": 1,
        "total": 62
    },
    "_items": [
        {
            "patient_name": "tttt",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a796b7e71867e233ad332f1"
                }
            },
            "patient_id": "1",
            "updated_at": "06/02/2018 08:46:54",
            "_id": "5a796b7e71867e233ad332f1",
            "created_at": "06/02/2018 08:46:54",
            "_updated_total_seconds": 1517906814
        },
        {
            "patient_name": "aaa",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a82afdd71867e233ad332f2"
                }
            },
            "patient_id": "1",
            "updated_at": "13/02/2018 09:29:01",
            "_id": "5a82afdd71867e233ad332f2",
            "created_at": "13/02/2018 09:29:01",
            "_updated_total_seconds": 1518514141
        },
        {
            "patient_name": "sss",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a8d21f671867e6182cc4842"
                }
            },
            "patient_id": "3",
            "updated_at": "21/02/2018 07:38:30",
            "_id": "5a8d21f671867e6182cc4842",
            "created_at": "21/02/2018 07:38:30",
            "_updated_total_seconds": 1519198710
        },
        {
            "patient_name": "james bond",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a8fb5e071867e6182cc4843"
                }
            },
            "patient_id": "7",
            "updated_at": "23/02/2018 06:34:08",
            "_id": "5a8fb5e071867e6182cc4843",
            "created_at": "23/02/2018 06:34:08",
            "_updated_total_seconds": 1519367648
        },
        {
            "patient_name": "sss",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a8fb73771867e6182cc4844"
                }
            },
            "patient_id": "3",
            "updated_at": "23/02/2018 06:39:51",
            "_id": "5a8fb73771867e6182cc4844",
            "created_at": "23/02/2018 06:39:51",
            "_updated_total_seconds": 1519367991
        },
        {
            "patient_name": "sss",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a8fb79871867e6182cc4845"
                }
            },
            "patient_id": "3",
            "updated_at": "23/02/2018 06:41:28",
            "_id": "5a8fb79871867e6182cc4845",
            "created_at": "23/02/2018 06:41:28",
            "_updated_total_seconds": 1519368088
        },
        {
            "patient_name": "sss",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a8fb7e271867e6182cc4846"
                }
            },
            "patient_id": "3",
            "updated_at": "23/02/2018 06:42:42",
            "_id": "5a8fb7e271867e6182cc4846",
            "created_at": "23/02/2018 06:42:42",
            "_updated_total_seconds": 1519368162
        },
        {
            "patient_name": "sss",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a8fb83e71867e6182cc4847"
                }
            },
            "patient_id": "3",
            "updated_at": "23/02/2018 06:44:14",
            "_id": "5a8fb83e71867e6182cc4847",
            "created_at": "23/02/2018 06:44:14",
            "_updated_total_seconds": 1519368254
        },
        {
            "patient_name": "sss",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a8fb88771867e6182cc4848"
                }
            },
            "patient_id": "3",
            "updated_at": "23/02/2018 06:45:27",
            "_id": "5a8fb88771867e6182cc4848",
            "created_at": "23/02/2018 06:45:27",
            "_updated_total_seconds": 1519368327
        },
        {
            "patient_name": "sss",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a8fb8d171867e6182cc4849"
                }
            },
            "patient_id": "3",
            "updated_at": "23/02/2018 06:46:41",
            "_id": "5a8fb8d171867e6182cc4849",
            "created_at": "23/02/2018 06:46:41",
            "_updated_total_seconds": 1519368401
        },
        {
            "patient_name": "sss",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a8fb95171867e6182cc484a"
                }
            },
            "patient_id": "3",
            "updated_at": "23/02/2018 06:48:49",
            "_id": "5a8fb95171867e6182cc484a",
            "created_at": "23/02/2018 06:48:49",
            "_updated_total_seconds": 1519368529
        },
        {
            "patient_name": "sss",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a8fb9a971867e6182cc484b"
                }
            },
            "patient_id": "3",
            "updated_at": "23/02/2018 06:50:17",
            "_id": "5a8fb9a971867e6182cc484b",
            "created_at": "23/02/2018 06:50:17",
            "_updated_total_seconds": 1519368617
        },
        {
            "patient_name": "sss",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a8fc52071867e6182cc484c"
                }
            },
            "patient_id": "3",
            "updated_at": "23/02/2018 07:39:12",
            "_id": "5a8fc52071867e6182cc484c",
            "created_at": "23/02/2018 07:39:12",
            "_updated_total_seconds": 1519371552
        },
        {
            "patient_name": "aaa",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a8fcfe871867e6182cc484d"
                }
            },
            "patient_id": "1",
            "updated_at": "23/02/2018 08:25:12",
            "_id": "5a8fcfe871867e6182cc484d",
            "created_at": "23/02/2018 08:25:12",
            "_updated_total_seconds": 1519374312
        },
        {
            "patient_name": "james bond",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a8fd1fd71867e6182cc484e"
                }
            },
            "patient_id": "7",
            "updated_at": "23/02/2018 08:34:05",
            "_id": "5a8fd1fd71867e6182cc484e",
            "created_at": "23/02/2018 08:34:05",
            "_updated_total_seconds": 1519374845
        },
        {
            "patient_name": "aaa",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a8fd71d71867e6182cc484f"
                }
            },
            "patient_id": "1",
            "updated_at": "23/02/2018 08:55:57",
            "_id": "5a8fd71d71867e6182cc484f",
            "created_at": "23/02/2018 08:55:57",
            "_updated_total_seconds": 1519376157
        },
        {
            "patient_name": "aaa",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a8fd80871867e6182cc4850"
                }
            },
            "patient_id": "1",
            "updated_at": "23/02/2018 08:59:52",
            "_id": "5a8fd80871867e6182cc4850",
            "created_at": "23/02/2018 08:59:52",
            "_updated_total_seconds": 1519376392
        },
        {
            "patient_name": "sjs",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a936aca71867e6182cc4851"
                }
            },
            "patient_id": "5",
            "updated_at": "26/02/2018 02:02:50",
            "_id": "5a936aca71867e6182cc4851",
            "created_at": "26/02/2018 02:02:50",
            "_updated_total_seconds": 1519610570
        },
        {
            "patient_name": "sjs",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a937fa871867e6182cc4852"
                }
            },
            "patient_id": "5",
            "updated_at": "26/02/2018 03:31:52",
            "_id": "5a937fa871867e6182cc4852",
            "created_at": "26/02/2018 03:31:52",
            "_updated_total_seconds": 1519615912
        },
        {
            "patient_name": "hhuh",
            "_links": {
                "self": {
                    "title": "Testlist",
                    "href": "testlist/5a938e7371867e6182cc4853"
                }
            },
            "patient_id": "55",
            "updated_at": "26/02/2018 04:34:59",
            "_id": "5a938e7371867e6182cc4853",
            "created_at": "26/02/2018 04:34:59",
            "_updated_total_seconds": 1519619699
        }
    ],
    "_links": {
        "parent": {
            "title": "home",
            "href": "/"
        },
        "next": {
            "title": "next page",
            "href": "testlist?max_results=20&sort=updated_at&page=2&timestamp=1528184525000"
        },
        "last": {
            "title": "last page",
            "href": "testlist?max_results=20&sort=updated_at&page=4&timestamp=1528184525000"
        },
        "self": {
            "title": "testlist",
            "href": "testlist?max_results=20&sort=updated_at&timestamp=1528184525000"
        }
    }
    }
    ```
 
* **Error Response:**

  <_Most endpoints will have many ways they can fail. From unauthorized access, to wrongful parameters etc. All of those should be liste d here. It might seem repetitive, but it helps prevent assumptions from being made where they should be._>


* **Sample Call:**

    * **request:** <br />GET http://{Server}/testlist?sort=-updated_at&max_results=20&timestamp=1528184525000
    
    OR
    
    * **request:** <br />GET http://{Server}/testlist/where={“patient_id”=”1”}&page=1&max_results=20

* **Notes:**

  <_This is where all uncertainties, commentary, discussion etc. can go. I recommend timestamping and identifying oneself when leaving comments here._> 