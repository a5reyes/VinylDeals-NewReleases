from flask import Flask, request, render_template
import vinyls
import re

app = Flask(__name__)

def get_link(res):
    results = str(res)
    info = results.split(" - ")
    artist = info[0]
    url_pattern = r'(https?://[^\s]+)'
    if "www.amazon" in res or "a.co" in res:
        tag = "..."
        return re.sub(url_pattern, r'<a href="\1' + tag + '" target="_blank">' + '<button>' + artist  + '</button>' + '</a>', res)
    else:
        return re.sub(url_pattern, r'<a href="\1" target="_blank">' + '<button>' + artist + '</button> </a>', res)

app.jinja_env.filters['get_link'] = get_link

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    else:
        if "deals" in request.form:
            sub_deals = "deals"
            limit_deals = get_limit()
            sub = vinyls.get_reddit(sub_deals, limit_deals)
            selected_sort = request.form.get("dropdown-sort")
            if selected_sort:
                if selected_sort == "price-low":
                    as_order = "ascending"
                    price_low = vinyls.sort_prices(sub, as_order)
                    return render_template("index.html", results=price_low)
                elif selected_sort == "price-high":
                    des_order = "descending"
                    price_high = vinyls.sort_prices(sub, des_order)
                    return render_template("index.html", results=price_high)
                elif selected_sort == "lps":
                    multi_lps = vinyls.num_vinyl(sub)
                    return render_template("index.html", results=multi_lps)
                elif selected_sort == "size":
                    sizes = vinyls.size_vinyl(sub)
                    return render_template("index.html", results=sizes)
            def_deals = vinyls.return_res(sub, sub_deals)
            return render_template("index.html", results=def_deals)
        else:
            sub_releases = "releases"
            limit_releases = get_limit()
            releases = vinyls.get_reddit(sub_releases, limit_releases)
            new_releases = vinyls.return_res(releases, sub_releases)
            return render_template("index.html", results=new_releases)

def get_limit():
    selected_limit = request.form.get("dropdown-limit")
    if selected_limit:
        if selected_limit == "20":
            limit_20 = "20"
            return limit_20
        if selected_limit == "50":
            limit_50 = "50"
            return limit_50
        if selected_limit == "100":
            limit_100 = "100"
            return limit_100
        if selected_limit == "200":
            limit_200 = "200"
            return limit_200
    else:
        limit = "10"
        return limit

if __name__ == '__main__':
    app.run(debug=True)
