<h2>Description</h2>

<p>Let's add the ability to remove cards from the site. To do so, you need to make a request with a city database id to the server. Also, just in case a user has put the wrong city name in the request, you need to send an error message to the user.</p>

<h2>Theory</h2>

<p>Flask can obtain values from the request URL. Below is an example of how you can take a city id from the URL and delete it from the database:</p>

<pre><code class="language-python">@app.route('/delete/&lt;city_id&gt;', methods=['GET', 'POST'])
def delete(city_id):
    city = City.query.filter_by(id=city_id).first()
    db.session.delete(city)
    db.session.commit()
    return redirect('/')</code></pre>

<p>It takes a city id from the route, deletes it from the database, and redirects a user to the main page.</p>

<p>Also, Flask can send flash messages to the user by passing a message in the <code class="language-python">flash()</code> method:</p>

<pre><code class="language-python">from flask import flash

...

@app.route('/', methods=['POST'])
def add():
    ...
    if city == None:
        flash("The city doesn't exist!")
    return redirect('/')</code></pre>

<p>After that, you can show the message in the template:</p>

<pre><code class="language-html">{% with message = get_flashed_messages() %}
{% if message %}
&lt;div class="alert alert-primary" role="alert"&gt;
    {{message[0]}}
&lt;/div&gt;
{% endif %}
{% endwith %}</code></pre>

<h2>Objectives</h2>

<p>Handle the wrong input:</p>

<ul>
	<li>If the user enters a city name that doesn't exist, output the following message: <code class="language-python">The city doesn't exist!</code></li>
	<li>If the user enters a city name that has already been added to the database, output the following message: <code class="language-python">The city has already been added to the list!</code></li>
</ul>

<p>Add the ability to delete cards. Each card should contain a form with a button inside. When the button is pressed, make a POST or a GET request to the server with a city id. For example, <code class="language-python">/delete/{{city.id}}</code>. This class is <code class="language-python">delete-button</code>. On the server side, take a city id, delete it from the database, and redirect a user to the main page.</p>