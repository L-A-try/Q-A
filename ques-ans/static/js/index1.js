var opts = {
	lines : 13, // 花瓣数目
	length : 20, // 花瓣长度
	width : 10, // 花瓣宽度
	radius : 30, // 花瓣距中心半径
	corners : 1, // 花瓣圆滑度 (0-1)
	rotate : 0, // 花瓣旋转角度
	direction : 1, // 花瓣旋转方向 1: 顺时针, -1: 逆时针
	color : 'black', // 花瓣颜色
	speed : 1, // 花瓣旋转速度
	trail : 60, // 花瓣旋转时的拖影(百分比)
	shadow : false, // 花瓣是否显示阴影
	hwaccel : false, // spinner 是否启用硬件加速及高速旋转
	className : 'spinner', // spinner css 样式名称
	zIndex : 2e9, // spinner的z轴 (默认是2000000000)
	top : 'auto', // spinner 相对父容器Top定位 单位 px
	left : 'auto'// spinner 相对父容器Left定位 单位 px
};

var spinner = new Spinner(opts);

var subjectStr = null;
var predicateStr = null;
var accusativeStr = null;

$(document).ready(function() {
	$("body").keydown(function() {
		 if (event.keyCode == "13") {//keyCode=13是回车键
			 $('#search').click();//换成按钮的id即可
		 }
	 });
	$("#search").bind("click", function() {
		ajaxRequestData();
	});
	$(".topQuestion").hide();
	var id = $("#send_type").val();
	$("#" + id).show();

	$("#course").bind("change", function() {
		$(".topQuestion").hide();
		var id = $("#send_type").val();
		$("#" + id).show();
		$(".result").text("");
		$("#inputQuestion").attr("placeholder", "");
		$("#inputQuestion").val("");
		$("#answerd fieldset").css("display", "none");
	});

	$(".ques").bind("click", function() {
		$("#inputQuestion").val($(this).text());
		ajaxRequestData();
	});

	$(".nav_t ul li").bind('click', function(){
		$(".nav_t ul li a").css('color', '#136EC2');
		$(".nav_t ul li").css('background-color', '');
		// this.css('background-color', '#136EC2');
		$(this).find('a').css('color', '#FFF')
		// this.style.color="#FFF";
		this.style.backgroundColor="#33bbee";
	})
});

function ajaxRequestData() {
	$("input[name='isvaluable']").attr("checked", false);
	var input_data = $("#inputQuestion").val();

	if(input_data == null || input_data == ""){
		input_data = $("#inputQuestion").attr('placeholder');
	}
	$.ajax({
		async:false,
		type : "POST",
		url : "/index_recv_data/",
		data : {
			inputQuestion : input_data,
			course : $("#send_type").val(),
			tupu_type: $("#course").val()
		},
		timeout : 6000,
		beforeSend : function() {
			// 异步请求时spinner出现
			$("#imformation").text("");
			var target = $("#wait").get(0);
			$("#answerd fieldset").css("display", "none");
			spinner.spin(target);
		},
		success : function(data) {
			// 关闭spinner
			spinner.spin();
			show();

			// 格式化显示数据
			data_exhibition(data);
			$("#research").show();
			// 显示答案
			$("#answerd").css('display', 'inline-block')
		},
		error : function(e, jqxhr, settings, exception) {
			$("#imformation").text("");
			$(".result").text("");
			$("#box").empty();
			$("#answerd fieldset").css("display", "block");
			$("#imformation").text("此问题没有找到答案");
			spinner.spin();
		}
	})
}

// 渲染知识图谱
function render(t1_text, t2_text) {
	try {
		$("svg").remove();
		var data = {};

		data.nodes = JSON.parse(t1_text);
		data.links = JSON.parse(t2_text);
		console.log(data.nodes)
		console.log(data.links)
		var config = {
			//鼠标mouseover后的弹窗
			content: null,
			contentHook: null,
			//节点配色方案（可为空)
			nodeColor: null,
			//连接线配色方案（可为空）
			linkColor: null,
			width: document.getElementById("container").clientWidth,
			height: document.getElementById("container").clientHeight
		}
		initKG(data, config, "#container")
	} catch (err) {
		Materialize.toast('渲染存在异常', 2000);
		console.log(err);
	}
}

// 根据后台传来的数据进行格式化显示
function data_exhibition(data) {
	// 显示结果
	// 代表查公司
	if(data.baseinfo_type == 0){
		// 需要显示的模块class name
		var class_name_list = ['message_jiben', 'zhuanli', 'message_Crj', 'message_Czp', "message_Fkt", "message_Fsf"]
		for(var i =0; i < class_name_list.length; i++){
			class_name = class_name_list[i];
			tmp_data = data[class_name];

			if(class_name == 'message_jiben'){
				var tmp_tag = document.getElementById('message_jiben_result');
				var result_text = "<table class='baseinfo_table table table-bordered'><tbody><tr><td style=\"width: 120px;\">公司名称</td><td>"+ tmp_data.name +"</td>";
				delete tmp_data.name;
				var 经营范围 = "<tr><td style=\"width: 120px;\">经营范围</td>" + "<td colspan=\"4\">" +tmp_data.经营范围+"</td></tr>";
				delete tmp_data.经营范围;
				var point = 1; // 用来换行
				for(var j in tmp_data){
					if(point%2 == 0){
						result_text += "</tr><tr>"
					}
					result_text += "<td style=\"width: 120px;\">"+j + "</td>" + "<td>" +tmp_data[j] + "</td>";
					point += 1;
				}
				result_text += "</tr>" + 经营范围 + "</tbody></table>"
				tmp_tag.innerHTML = result_text;
				$("."+class_name).css('display', 'block')
			}
			else{
				var tmp_table = document.getElementById(class_name+"_result");
				if(tmp_data.length == 0){continue}
				// console.log(tmp_data)
				var key_list = Object.keys(tmp_data[0]);
				var table_data = "";
				// 构建表格的表头
				table_data = '<table class="'+class_name+'_table table table-bordered'+'"><thead><tr>'
				for(var key in key_list){
					table_data += '<th>'+key_list[key]+'</th>'
				}
				table_data += '</tr></thead><tbody>'
				// 构建表格的表体
				for(var dic_list_index in tmp_data){
					table_data += '<tr>'
					var dic_list = tmp_data[dic_list_index];
					for(var k =0; k < key_list.length; k++){
						var key1 = key_list[k];
						var value = dic_list[key1];
						table_data += '<td>'+value+'</td>'
					}
					table_data += '</tr>'
				}
				table_data += '</tbody></table>';
				tmp_table.innerHTML = table_data;
				$('.'+class_name+"_table").dynatable();
				$("."+class_name).css('display', 'block');
			}
		}
	}
	else if(data.baseinfo_type == 1){//代表查老板
		$("#message_jiben_result").html(data.result);
		$(".message_jiben").css('display', 'block');
	}
	else if(data.baseinfo_type == 2){//代表查知识问答
		$("#message_jiben_result").html(data.result);
		$(".message_jiben").css('display', 'block');
	}
	else if(data.baseinfo_type == 3){//代表查知识图谱

	}

	var t1_text = data.t1_text;
	var t2_text = data.t2_text;

	// 如果不为空，则显示图谱 if(t1_text != '' | t1_text != null)???????????????????????????????????????????????????????没有图 却显示这个模块
	if(t2_text.length!==0 ){
		$(".zhishitupu").css('display', 'block')
		render(t1_text, t2_text);

	}
}

function show() {
	var length = 100;
	$(".list").each(function() {
		var text = $(this).html();
		if (text.length < 200)
			return;
		var newBox = document.createElement("div");// 创建一个新的div对象。
		var btn = document.createElement("a");// 创建一个新的a对象。
		if (text.indexOf("--") > 0 && text.indexOf(":") > 0) {
			var array = text.split(":");
			text = "<b>" + array[0] + ":</b>" + array[1];
		}
		newBox.innerHTML = text.substring(0, length);
		btn.innerHTML = text.length > length ? " ...显示全部" : "";
		btn.href = "###";
		btn.onclick = function() {
			if (btn.innerHTML == " ...显示全部") {
				btn.innerHTML = " 收起";
				newBox.innerHTML = text;
				newBox.append(btn);
			} else {
				btn.innerHTML = " ...显示全部";
				newBox.innerHTML = text.substring(0, length);
				newBox.append(btn);
			}
			MathJax.Hub.Queue([ "Typeset", MathJax.Hub ]);
		}
		$(this).text("");
		$(this).append(newBox);
		newBox.append(btn);
	});
}

function choice_type(ty){
	if(ty == 1){
		$("#inputQuestion").css('display', 'inline-block')
		$("#course").css('display', 'none');
		$("#inputQuestion").val('上海找钢网信息科技股份有限公司');
		$("#send_type").val('chinese');
		// 将所有相关的问题都隐藏
		$(".topQuestion").css('display', 'none');
		// 单独显示当前相关的问题
		$("#chinese").css('display', 'block');
		// 隐藏答案
		$(".fieldset").css('display', 'none')
	}
	else if(ty==2){
		$("#inputQuestion").css('display', 'inline-block')
		$("#course").css('display', 'none');
		$("#inputQuestion").val('郁亮');
		$("#send_type").val('history')
		$(".topQuestion").css('display', 'none');
		$("#history").css('display', 'block');
		$(".fieldset").css('display', 'none')
	}
	else if(ty==3){
		$("#inputQuestion").css('display', 'inline-block')
		$("#course").css('display', 'none');
		$("#send_type").val('question');
		$("#inputQuestion").val('');
		$(".topQuestion").css('display', 'none');
		$(".fieldset").css('display', 'none')
	}
	else if(ty==4){
		$("#inputQuestion").css('display', 'none')
		$("#send_type").val('tupu');
		$("#course").css('display', 'inline-block')
		$("#course").val('tupu_chinese');
		$(".topQuestion").css('display', 'none');
		$("#inputQuestion").val('');
		$(".fieldset").css('display', 'none')

	}
}
