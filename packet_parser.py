def parse() :
	for item in filenames:
		read_data(item, filenames[item])
	return filenames

def read_data(file_name, L):
	f = open(file_name, 'r')
	lines = f.readlines()
	[L.append(line.strip()) for line in lines]
	for node in nodes:
		for line in lines:
			line = line.strip()
			if node in line:
				if "Echo (ping) request" in line:
					nodes[node][0].append(line)
				elif "Echo (ping) reply" in line:
					nodes[node][1].append(line)
	f.close()

nodes = {
	"192.168.100.1         192.168": [[],[]],
	"192.168.100.2         192.168": [[],[]],
	"192.168.200.1         192.168": [[],[]],
	"192.168.200.2         192.168": [[],[]]
}

filenames = {
	"Node1_filtered.txt": [],
	"Node2_filtered.txt": [],
	"Node3_filtered.txt": [],
	"Node4_filtered.txt": []
}