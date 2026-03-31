def handle_request(response):
    try:
        request = response.request
        url = request.url
        method = request.method

        post_data = None
        try:
            post_data = request.post_data
        except:
            pass

        if any(x in url for x in ["SWS", "search", "claim", "query"]):
            print("\n🔥 REQUEST CAPTURED")
            print("METHOD:", method)
            print("URL:", url)
            print("POST DATA:", post_data)

        # still capture JSON responses
        try:
            if "application/json" in response.headers.get("content-type", ""):
                data = response.json()
                self.captured_payloads.append({
                    "url": url,
                    "method": method,
                    "data": data
                })
        except:
            pass

    except:
        pass
