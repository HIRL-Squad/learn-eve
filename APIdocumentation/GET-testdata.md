**GET testdata**
----
Gets a testdata document by its ID 
* **URL**

  /testdata/[record id]

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:** None
 
   **Optional:** None

* **Data Params**

    None
    
* **Success Response:**
  
  * **Code:** 200 <br />
    **Content example:** 
    ```json
    {
    "patient_name": "sss",
    "_links": {
        "parent": {
            "title": "home",
            "href": "/"
        },
        "collection": {
            "title": "testdata",
            "href": "testdata"
        },
        "self": {
            "title": "Testdata",
            "href": "testdata/5b10e81871867e4e40dd50a6"
        }
    },
    "patient_id": "3",
    "updated_at": "01/06/2018 06:30:48",
    "_id": "5b10e81871867e4e40dd50a6",
    "human_correction": {
        "36": "4"
    }, 
    "created_at": "01/06/2018 06:30:48",
    "test": [please see the testdata_format document]
    }
    ```
 
* **Error Response:**

  <_Most endpoints will have many ways they can fail. From unauthorized access, to wrongful parameters etc. All of those should be liste d here. It might seem repetitive, but it helps prevent assumptions from being made where they should be._>
  * **Code:** 404 NOT FOUND <br />
    **Content:** 
    ```json
    {
    "_status": "ERR",
    "_error": {
        "message": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.",
        "code": 404
    }
    }
    ```

* **Sample Call:**

    * **request:** <br />GET http://{Server}/testdata/5b10e81871867e4e40dd50a6
            
* **Notes:**

  <_This is where all uncertainties, commentary, discussion etc. can go. I recommend timestamping and identifying oneself when leaving comments here._> 