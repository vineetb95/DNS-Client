# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, url_for, Markup, redirect
import dns.message
import dns.query
import dns.flags

# function to create a table row with elements in lis, id clasi and width =size


def make_row(lis, clasi, size=90):
    stri = "<div class='row' style='width:" + \
        str(size)+"%; display: flex;justify-content: space-between;border-collapse: collapse;'>\n"
    for k in lis:
        if k != None:
            k = "<br><br>".join(k.splitlines())
        stri = stri+"<div class='cell' style='padding:3px 0;width: 100%;text-align:center;  float:left;border-left:1px solid white;border-top:1px solid white;border-bottom:1px solid white;'>" + \
            str(k)+"</div>\n"

    stri = stri+"<div data-title='"+clasi+"' class='info' style='padding:3px 6px 3px 0;border-right:1px solid white;border-top:1px solid white;border-bottom:1px solid white;'><i class='fa fa-info-circle' style='font-size:24px'></i></div>"
    stri = stri+"</div>\n"

    return stri


# making html for the table representation
def make_table(u):
    opcode = dns.message.dns.opcode.to_text(u.opcode())
    rcode = dns.message.dns.rcode.to_text(u.rcode())
    flags = dns.message.dns.flags.to_text(u.flags).split(" ")
    questions = u.question[0].to_text()
    print(u.to_text())
    answers = [u.answer[0].to_text() if len(u.answer) > 0 else None]
    authoritys = [u.authority[0].to_text() if len(u.authority) > 0 else None]
    # additionals = [u.additional[0].to_text() if len(u.additional)
    #                > 0 else None]
    if(len(u.additional) > 0):
        additionals = [u.additional[i].to_text()
                       for i in range(len(u.additional))]
    else:
        additionals = [None]

    # print("this should yield", u.additional[1].to_text())

    # print("addition", additionals)
    stri = ''

    stri = stri+make_row([opcode, rcode], "opcode & rcode")
    stri = stri+make_row(flags, "flags")
    stri = stri+make_row([questions], "question")
    for answer in answers:
        stri = stri+make_row([answer], "answers")

    for authority in authoritys:
        stri = stri+make_row([authority], "authority")

    str1 = ""
    for additional in additionals:
        if(additional != None):
            str1 += additional+"\n"
        else:
            str1 = None
    stri = stri+make_row([str1], "additional")

    return stri


def my_dns_query(hostname, query_type, recrusion_desire, server, portNo, tk=2):
    query = dns.message.make_query(hostname, query_type)

    if(not recrusion_desire):
        query.flags ^= dns.flags.RD

    query_response = dns.query.udp(
        query, server, port=int(portNo), timeout=int(tk))
    print(query_response)

    return make_table(query_response)


app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
# ‘/’ itial values set to google.com 8.8.8.8 recursion desire A
def hello_world():
    return render_template("index.html", params=["www.google.com", "8.8.8.8", ["checked", "", "", "", "",
                                                                               "", "", "", "", "", ""], "checked"], answer="", port="", timeout="")


@app.route('/favicon.ico/', methods=['GET', ])
def favicon():
    # just returning the icon of the website
    return app.send_static_file("favicon.ico")


@app.route("/search")
def search():
    try:
        hostname = request.args.get('hostname')
        query_type = request.args.get('query_type')
        recrusion_desire = request.args.get('rd')
        portNo = request.args.get('port')
        if(portNo == ""):
            portNo = "53"
        tk = request.args.get('timeout')
        if(tk == ""):
            tk = "2"
        if(recrusion_desire == "on"):
            rd = True
        else:
            rd = False

        server = request.args.get("server")
        lis = ["A", "AAAA", "MX", "ANY", "CNAME",
               "CAA", "NS", "PTR", "SOA", "SRV", "TXT"]

        send_list = [""for x in range(len(lis))]
        send_list[lis.index(query_type)] = "checked"

        if(recrusion_desire == "on"):
            rd1 = "checked"
        else:
            rd1 = ""

        # Markup function convert text to html so it can be used in jinja as html not as text
        return render_template("index.html", params=[hostname, server, send_list, rd1], answer=Markup(my_dns_query(hostname, query_type, rd, server, portNo, tk)), port=portNo, timeout=tk)

    except Exception as e:
        print(e)
        return render_template("index.html", params=["", "", ["checked", "", "", "", "",
                                                              "", "", "", "", "", ""], "checked"], answer="", reError="Yes", port="", timeout="")


if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
