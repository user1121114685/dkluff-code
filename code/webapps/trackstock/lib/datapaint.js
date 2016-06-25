function g2paint_c1(d) {
    var data = datatoJSON(d)
    var chart = new G2.Chart({ // 声明一个图表
        id: 'c1',
        width: 800,
        height: 400,
        plotCfg: {
          margin: 80, // 设置 margin
          border: {
            stroke: '#ddd',
            'stroke-width': 3, // 设置线的宽度
            radius: 10 // 设置圆角
          }, // 设置边框
          background : {
            fill: '#3F3F4F'
          } // 设置背景色
        }
    });
    chart.source(data);
    chart.col('count',{type: 'linear',min:0})
    chart.interval().position('gender*count').color('gender').size(60);
    chart.render();
}