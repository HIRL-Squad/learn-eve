**POST testdata**
----
Upload a testdata document to the server
* **URL**

  /testdata

* **Method:**

  `POST`
  
*  **URL Params**

   **Required:** None
 
   **Optional:** None

* **Data Params**

    ```json
    {
    "human_correction": {
        "36": "4"
    },
    "test": [please see testdata_format for detail]
    }
    ```
    
* **Success Response:**
  
  * **Code:** 201 CREATED <br />
    **Content example:** 
    ```json
    {
    "updated_at": "07/06/2018 08:35:23",
    "created_at": "07/06/2018 08:35:23",
    "_id": "5b18ee4b6eae6ab46ea3caf8",
    "_links": {
        "self": {
            "title": "Testdata",
            "href": "testdata/5b18ee4b6eae6ab46ea3caf8"
        }
    },
    "_status": "OK"
    }
    ```
 
* **Error Response:**

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

    * **request:** <br />POST http://{Server}/testdata/
    * **body:**
        ```json
        {
        "human_correction": {
            "36": "4"
        },
        "test": [please see testdata_format for detail]
        }
        ```
            
* **Notes:**

  <_This is where all uncertainties, commentary, discussion etc. can go. I recommend timestamping and identifying oneself when leaving comments here._> 