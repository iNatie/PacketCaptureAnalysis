def read_data(file_name, L):
	f = open(file_name, 'r')
	[L.append(line.strip()) for line in f.readlines() if "icmp" in line.strip().lower() and "unreachable" not in line.strip().lower()]
	f.close()

def write_data(file_name, file_data):
	file_name = file_name.split(".txt")[0]
	file_name = f"{file_name}_filtered.txt"
	f = open(file_name, 'w')
	f.writelines('\n'.join(file_data))
	f.close()

def filter() :
	for item in filenames:
		read_data(item, filenames[item])
		write_data(item, filenames[item])
	
Node1 = []
Node2 = []
Node3 = []
Node4 = []

filenames = {
	"Node1.txt": Node1,
	"Node2.txt": Node2,
	"Node3.txt": Node3,
	"Node4.txt": Node4
}