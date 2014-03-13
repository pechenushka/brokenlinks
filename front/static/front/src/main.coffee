class Links
  constructor: (options) ->
    @loader = new Loader()
    @links = [options.url]
    @status_colors =
      '200': 'green'
      '404': 'red'
    @resource_types = options.resource_types

  get_links: (url = null, parent_url = null) ->
    @loader.load_show()

    # Если не указан урл - значит это первый запуск
    url = url || @links[0]
    resource_types = @resource_types

    $.get('/get_links/', { url, resource_types }, (response) =>
      @loader.load_hide()

      if response.error
        Alert.error response.message
      else
        @fill_links(response, url)
        Alert.success 'Связи успешно загружены'

    ).error (err) ->
      @loader.load_hide()
      Alert.error err.statusText

  fill_links: (links, parent_url = null) ->
    $(links).each (key, obj) =>

      if $.inArray(obj.href, @links) < 0
        @links.push obj.href

        if $.inArray(obj.type, @resource_types.split(',')) != -1
          obj.color = @status_colors[obj.status]
          $("#link_el_template").tmpl(obj).appendTo("#links")

        if not obj.is_file and obj.status == '200'
          @get_links(obj.href)

class Loader
  load_show: ->
    $("#loader").show()
    $("#button_back").hide()

  load_hide: ->
    $("#loader").hide()
    $("#button_back").show()

window.Links = Links
window.Loader = Loader