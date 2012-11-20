$(document).ready(function() {

    $('#cadastro-paciente').submit(function(event) {
        event.preventDefault();

        $("#enviando").attr('rel', 'gallery').fancybox({
            beforeShow: function() {
                $(".fancybox-skin").css("backgroundColor", "black");
            },
            'padding': 0,
            'margin': 0,
            'height': 2,
            'modal': true,
            'opacity': true,
            'openEffect': 'elastic',
            'closeEffect': 'elastic',
        }).click();

        var $form = $(this),
            url = $form.attr('action');

        $.post(url, $form.serialize(), function(data) {
            parent.$.fancybox.close();
           $('#cadastro-usuario').html(data);
        });
    });

});

