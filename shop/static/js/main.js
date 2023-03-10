$(".plus_cart").click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    console.log("pid", id);
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id,
        },
        success: function (data) {
            eml.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        },
    });
});

$(".minus_cart").click(function () {
    var id = $(this).attr("pid").toString();
    var el = this.parentNode.children[2];
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id,
        },
        success: function (data) {
            console.log(data);
            el.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        },
    });
});
