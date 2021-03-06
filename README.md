
<h1>TRADING REGISTRY</h1>
<h3>REQUIREMENTS</h3>
<P><a href="https://www.docker.com/"><b>docker</b></a> with <a href="https://docs.docker.com/compose/install/"><b>docker-compose</b></a>; and the type: "docker-compose up"</P>
<p>After the process the web will be available at <a href="http://localhost/">localhost</a></p>
<p></p>
<h3>USERS</h3>
<p>There are 2 pregenerated users in te system:</p>
    <ul>
        <li><p><b>( monobot / admin )</b> is the django superuser, you can access the administration site <a href="{% url 'admin:index' %}">here</a></p></li>
        <li><p><b>( plain_user / admin )</b> is a regular user you can use to see and create trades</p></li>
    </ul>
<p>A very basic user creation and change password exists, so you can generate your own users if you like it so.</p>
<h3>Trading</h3>
<h4>Model considerations:</h4>
<p>The indentificator is a unique field in the database, to generate the alphanumeric hash the item id and book date are used. To avoid collisions (not that low for 7 characters) there is a fail proof recursive method that checks before the save.</p>
<h4>Trading system considerations:</h4>
<p>When the system starts a django command is launched to save all the different currencies changes and stores them in the redis cache. </p>
<p>But when the trade is booked its checked again right before the save in the database to get the most updated rate in the very same moment of the save, if the external api is not available in the time of the save the transaction is declined.</p>
<p>Althought the frontend also checks the exchange rate in real time (first gets the rate from the cache and then updates with the latest). its not considered secure to take that data as correct and so both the rate and buy_amount are not available fields in the api.</p>
<p>Examples of possible exploits avoided with that:</p>
<ul>
    <li>Someone sets the trade and then waits hours before clicking the save button, and doing the same thing with other currencies can exploit the system getting great profit</li>
    <li>If the api is public (or vulnerable) they can manually set the rate and/or buy_amount and so buy without the real money required</li>
</ul>
<h3>DOCKERIZATION</h3>
<p>The application is divided into 5 docker containers</p>
<table class="table table-striped table-hover">
    <thead>
        <th>application</th>
        <th>container name</th>
        <th>autostart</th>
    </thead>
    <tbody>
        <tr>
            <td><b>postgres</b></td>
            <td>db_eb_postgres</td>
            <td>yes</td>
        </tr>
        <tr>
            <td><b>redis</b></td>
            <td>redis_cache</td>
            <td>yes</td>
        </tr>
        <tr>
            <td><b>django</b></td>
            <td>django</td>
            <td>yes</td>
        </tr>
        <tr>
            <td><b>nginx</b></td>
            <td>webserver</td>
            <td>yes</td>
        </tr>
        <tr>
            <td><b>testing</b></td>
            <td>db_eb_testing</td>
            <td>no</td>
        </tr>
    </tbody>
</table>
<br>
<p>To lower a bit the container isolation, I have done the next:</p>
<h4>logging</h4>
<p>The <b>django</b>, de <b>nginx</b> and <b>gunicorn</b> log files are stored on <b>logs/</b> directory of the host OS</p>
<br>
<h4>database</h4>
<p>A fabric command will create a database backup into <b>db_backup/</b> directory</p>
<pre>../ebury_root$ fab db_backup</pre>
<br>
<h3>TESTING</h3>
<p>First start the docker testing database container (if its not already started):</p>
<pre>$ docker start db_eb_testing</pre>
<p>Also start the django container (if its not already started):</p>
<pre>$ docker start eburyroot_django</pre>
<p>Then we can run the tests</p>
<pre>$ docker exec -i -t eburyroot_django python manage.py test</pre>
<p>And lastly stop the testing database container (we will not automatically stop the django container)</p>
<pre>$ docker stop db_eb_testing</pre>
<br>
<p>To automatize the process there is also a fabric command</p>
<pre>../ebury_root$ fab test</pre>
<br>
