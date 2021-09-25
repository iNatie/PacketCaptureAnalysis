def compute(parsed_data) :
	with open('output.csv', 'w') as f:
		for item in parsed_data:
			print(f"*** {item} ***")
			parsed_name = item.split(" ")[0].split("_")[0]
			request_stats = calc_req_reply(parsed_data[item], node_addresses[item])
			print(f"Echo Requests Sent: {request_stats[0]}")
			print(f"Echo Requests Received: {request_stats[1]}")
			print(f"Echo Replies Sent: {request_stats[2]}")
			print(f"Echo Replies Received: {request_stats[3]}")
			bytes_data = sum_bytes(parsed_data[item], node_addresses[item], node_reply_addresses[item])
			bytes_sum = sum_frames(parsed_data[item], node_addresses[item])
			data_sum = sum_data(parsed_data[item], node_addresses[item])
			rtt = round_trip_time(parsed_data[item], node_addresses[item])
			sum_trip = rtt[0]
			avg_rtt = rtt[1]
			echo_request_throughput = round(((bytes_sum / sum_trip) / 1000), 1)
			echo_request_goodput = round(((data_sum / sum_trip) / 1000), 1)
			print(f"Echo Request Throughput (kB/sec): {echo_request_throughput}")
			print(f"Echo Request Goodput (kB/sec): {echo_request_goodput}")
			avg_reply = avg_reply_delay(parsed_data[item], node_reply_addresses[item])
			avg_ttl = time_to_live(parsed_data[item], node_addresses[item])
			f.write(f"{parsed_name}\n\nEcho Requests Sent,Echo Requests Received,Echo Replies Sent,Echo Replies Received\n{request_stats[0]},{request_stats[1]},{request_stats[2]},{request_stats[3]}\n")
			f.write(f"Echo Request Bytes Sent (bytes),Echo Request Data Sent (bytes)\n{bytes_data[0]},{bytes_data[2]}\n")
			f.write(f"Echo Request Bytes Received (bytes),Echo Request Data Receieved (bytes)\n{bytes_data[1]},{bytes_data[3]}\n\n")
			f.write(f"Average RTT (milliseconds),{avg_rtt}\nEcho Request Throughput (kB/sec),{echo_request_throughput}\nEcho Request Goodput,{echo_request_goodput}\nAverage Reply Delay,{avg_reply}\nAverage Echo Request Hop Count,{avg_ttl}\n\n")
			print("\n")
		f.close()


def sum_bytes(L, request_data, reply_data):
	request_bytes_sent = sum([int(line.split("ICMP")[1].split("Echo")[0].strip()) for line in L if request_data["request"] in line and "Echo (ping) request" in line])
	request_bytes_received = sum([int(line.split("ICMP")[1].split("Echo")[0].strip()) for line in L if reply_data["reply"] in line and "Echo (ping) reply" in line])
	request_data_sent = sum([(int(line.split("ICMP")[1].split("Echo")[0].strip()) - 42) for line in L if request_data["request"] in line and "Echo (ping) request" in line])
	request_data_received = sum([(int(line.split("ICMP")[1].split("Echo")[0].strip()) - 42) for line in L if reply_data["reply"] in line and "Echo (ping) reply" in line])
	print(f"Total Echo Request Bytes Sent: {request_bytes_sent}")
	print(f"Total Echo Request Bytes Received: {request_bytes_received}")
	print(f"Total Echo Request Data Sent: {request_data_sent}")
	print(f"Total Echo Request Data Received: {request_data_received}")
	return request_bytes_sent, request_bytes_received, request_data_sent, request_data_received

def sum_frames(L, machine_data):
	return sum([int(line.split("ICMP")[1].split("Echo")[0].strip()) for line in L if machine_data["request"] in line and "Echo (ping) request" in line])

def sum_data(L, machine_data):
	return sum([(int(line.split("ICMP")[1].split("Echo")[0].strip()) - 42) for line in L if machine_data["request"] in line and "Echo (ping) request" in line])

def parse_timestamp(line):
	return float(line.split(" ")[1].split("192.168")[0].strip())

def parse_ttl(line):
	return float(line.split("ttl=")[1].split(" ")[0])

def echo_sent(L):
	return len([item for item in L if ""])

def round_trip_time(L, machine_data):
	list_of_requests = [line for line in L if "reply in" in line.strip() if machine_data["request"] in line]
	list_of_replies = [line for line in L if "request in" in line.strip() if machine_data["reply"] in line]

	list_of_elapsed = []

	for i in range(len(list_of_requests)):
		replies_line = list_of_replies[i]
		requests_line = list_of_requests[i]
		packet_id = replies_line.split(" ")[0]
		elapsed = round(parse_timestamp(list_of_replies[i]) - parse_timestamp(list_of_requests[i]), 6)
		list_of_elapsed.append(elapsed)

	avg_rtt = round((sum(list_of_elapsed) / len(list_of_elapsed)) * 1000, 2)
	sum_elapsed = sum(list_of_elapsed)
	print(f"Average RTT: {avg_rtt}")
	return sum_elapsed, avg_rtt

def time_to_live(L, machine_data):
	list_of_requests = [line for line in L if "reply in" in line.strip() if machine_data["request"] in line]
	list_of_replies = [line for line in L if "request in" in line.strip() if machine_data["reply"] in line]

	hops = []

	for i in range(len(list_of_requests)):
		reply_ttl = parse_ttl(list_of_replies[i])
		request_ttl = parse_ttl(list_of_requests[i])
		current_hops = (request_ttl - reply_ttl) + 1
		hops.append(current_hops)

	average_hops = round(sum(hops) / len(hops), 2)
	print(f"Average Hops: {average_hops}")
	return average_hops

def avg_reply_delay(L, machine_data):
	list_of_requests = [line for line in L if "reply in" in line.strip() if machine_data["request"] in line]
	list_of_replies = [line for line in L if "request in" in line.strip() if machine_data["reply"] in line]

	list_of_elapsed = []

	for i in range(len(list_of_requests)):
		replies_line = list_of_replies[i]
		requests_line = list_of_requests[i]
		packet_id = replies_line.split(" ")[0]
		elapsed = round(parse_timestamp(list_of_replies[i]) - parse_timestamp(list_of_requests[i]), 6)
		list_of_elapsed.append(elapsed)

	avg_delay = round((sum(list_of_elapsed) / len(list_of_elapsed)) * 1000000, 2)
	print(f"Average Reply Delay: {avg_delay}")
	return avg_delay

def calc_req_reply(L, machine_data):
	requests_sent = len([line for line in L if machine_data["request"] in line and "Echo (ping) request" in line])
	requests_received = len([line for line in L if machine_data["reply"] in line and "Echo (ping) request" in line])
	replies_sent = len([line for line in L if machine_data["reply"] in line and "Echo (ping) request" in line])
	replies_received = len([line for line in L if machine_data["reply"] in line and "Echo (ping) reply" in line])
	return requests_sent, requests_received, replies_sent, replies_received

node_addresses = {
	"Node1_filtered.txt": {"request": "192.168.100.1         192.168", "reply": "192.168.100.1         ICMP"},
	"Node2_filtered.txt": {"request": "192.168.100.2         192.168", "reply": "192.168.100.2         ICMP"},
	"Node3_filtered.txt": {"request": "192.168.200.1         192.168", "reply": "192.168.200.1         ICMP"},
	"Node4_filtered.txt": {"request": "192.168.200.2         192.168", "reply": "192.168.200.2         ICMP"}
}

node_reply_addresses = {
	"Node1_filtered.txt": {"request": "192.168.100.1         ICMP", "reply": "192.168.100.1         192.168"},
	"Node2_filtered.txt": {"request": "192.168.100.2         ICMP", "reply": "192.168.100.2         192.168"},
	"Node3_filtered.txt": {"request": "192.168.200.1         ICMP", "reply": "192.168.200.1         192.168"},
	"Node4_filtered.txt": {"request": "192.168.200.2         ICMP", "reply": "192.168.200.2         192.168"}
}