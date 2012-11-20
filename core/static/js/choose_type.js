$(document).ready(function() {
    $('.tipo-cadastro').click(function(event) {

        event.preventDefault();

        var tipoUsuario = $(this).attr('data-tipo-usuario');
        var content = "";
        var target = ""

        switch(tipoUsuario) {
            case "paciente":
                target = "/contas/cadastro/paciente/";
                break;
            case "medico":
                target = "/contas/cadastro/medico/";
                break;
            case "clinica":
                target = "/contas/cadastro/clinica";
                break;
            default:
                target = "error"
        }

        if (target != "error") {
            $.get(target, function(data) {
                $('#cadastro-usuario').html(data);
            });
        }
        else {
            alert('Tipo de usuário inválido!');
        }
    });
});
