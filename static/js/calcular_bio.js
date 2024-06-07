document.addEventListener('DOMContentLoaded', function() {
    const peso = document.getElementById('peso');
    const altura = document.getElementById('altura');
    const imc = document.getElementById('imc');

    function calcularIMC() {
        let valor_peso = parseFloat(peso.value.trim());
        let valor_altura = parseFloat(altura.value.trim());

        if (!isNaN(valor_peso) && !isNaN(valor_altura) && valor_altura > 0) {
            let resultado = valor_peso / (valor_altura ** 2);
            imc.value = resultado.toFixed(2); // arredonda o resultado para 2 casas decimais
        } else {
            imc.value = ''; // limpa o valor se os inputs não forem válidos
        }
    }

    peso.addEventListener('input', calcularIMC);
    altura.addEventListener('input', calcularIMC);

});