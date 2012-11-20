$(document).ready(function() {
    $('select').change(function() {
        var especialidade = $(".especialidade").val();
        var clinica = $(".clinica").val();
        var url = '/home/3/medicos/'
        if(clinica != 'todas' && especialidade != 'todas') {
            $.get(url, {'especialidade': especialidade, 'clinica': clinica}, function(data) {
                $('#row3').replaceWith($(data).filter("#row3"));
            });
        }
        else if(clinica == 'todas') {
            $.get(url, {'especialidade': especialidade, 'clinica': ''}, function(data) {
                $('#row3').replaceWith($(data).filter("#row3"));
            });
        }
        else if(especialidade == 'todas') {
            $.get(url, {'especialidade': '', 'clinica': clinica}, function(data) {
                $('#row3').replaceWith($(data).filter("#row3"));
            });
        }
        else if (especialidade == 'todas' && clinica == 'todas') {
            $.get(url, {'nome' : '', 'especialidade': '', clinica: ''}, function(data) {
                $('row3').replaceWith($(data).filter("row3"));
            });
        }
    });
});
