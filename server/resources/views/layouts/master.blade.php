<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="icon" href="../../../../favicon.ico">

    <title>Album example for Bootstrap</title>

    <!-- Bootstrap core CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

    <!-- Custom styles for this template -->
    <link href="/css/album.css" rel="stylesheet">
  </head>

  <body>

    <div id="app">
      <nav class="navbar navbar-inverse">
      </nav>

      <section class="jumbotron text-center">
        <div class="container">
          <searchbar></searchbar>
        </div>
      </section>

      @yield('content')

      <footer class="text-muted">

      </footer>
    </div>

  <script src="{!! asset('js/app.js') !!}"></script>
  </body>
</html>
