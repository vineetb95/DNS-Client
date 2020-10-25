import dns.message
import dns.query
import dns.flags

def json_query(hostname, query_type, recrusion_desire, server, portNo, tk=2):
    query = dns.message.make_query(hostname, query_type)
    if(not recrusion_desire):
        query.flags ^= dns.flags.RD

    query_response = dns.query.udp(
        query, server, port=int(portNo), timeout=int(tk))

    opcode = dns.message.dns.opcode.to_text(query_response.opcode())
    rcode = dns.message.dns.rcode.to_text(query_response.rcode())
    flags = dns.message.dns.flags.to_text(query_response.flags).split(" ")
    questions = query_response.question[0].to_text()
    answers = [query_response.answer[0].to_text() if len(query_response.answer) > 0 else None]
    authorities = [query_response.authority[0].to_text() if len(query_response.authority) > 0 else None]
    if (len(query_response.additional) > 0):
        additionals = [query_response.additional[i].to_text()
                       for i in range(len(query_response.additional))]
    else:
        additionals = [None]
    response = {
        'opcode': opcode,
        'rcode' : rcode,
        'flags' : flags,
        'questions' : questions,
        'answers' : answers,
        'authorities' : authorities,
        'additionals' : additionals,
    }
    return response
