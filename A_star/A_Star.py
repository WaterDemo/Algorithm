class Node(object):
    """
    id represents the index of the point. eg: '[1,2]'

    """

    def __init__(self, id):
        self.id = id
        self.parent = None
        self.x = self.y = 0
        self.element = []
        self.__parse_coordinate()
        self.g_score = 0
        self.h_score = 0

    def __parse_coordinate(self):
        element = eval(self.id)
        self.element = element
        self.x = element[0]
        self.y = element[1]

    def f_value(self):
        return self.g_score + self.h_score

    def __lt__(self, other):
        return self.f_value() < other.f_value()


class A_Star(object):
    edge_limit = 20

    def __init__(self, obstacles, start, end):
        self.open_list = []
        self.close_list = []
        self.s_node = Node(start)
        self.e_node = Node(end)
        self.obstacles = self.__obsnode_list(obstacles)

    def hami_dist(self, node):
        return 10 * abs(node.x - self.e_node.x) + 10 * abs(node.y - self.e_node.y)

    def __obsnode_list(self, obstacles):
        nodes = []
        for item in obstacles:
            nodes.append(Node(item))
        return nodes

    def calcul(self):
        h_open_list = {}
        h_close_list = {}
        self.s_node.g_score = 0
        self.s_node.h_score = self.hami_dist(self.s_node)
        self.open_list.append(self.s_node)
        h_open_list[self.s_node.id] = self.s_node

        while len(self.open_list) > 0:
            self.open_list.sort()
            current_node = self.open_list[0]
            if current_node.id == self.e_node.id:
                return current_node
            node_list = self.gen_nodes(current_node)
            for node in node_list:
                current_cost = current_node.g_score + self.dis(node, current_node)
                if any(node.id == x.id for x in self.open_list):
                    in_node = h_open_list[node.id]
                    if in_node.g_score <= current_cost:
                        continue
                    else:
                        in_node.g_score = current_cost
                        in_node.parent = current_node
                elif any(node.id == x.id for x in self.close_list):
                    in_node = h_close_list[node.id]
                    if in_node.g_score <= current_cost:
                        continue
                    else:
                        self.close_list.remove(in_node)
                        h_close_list.pop(node.id)
                        in_node.g_score = current_cost
                        self.open_list.append(in_node)
                        h_open_list[in_node.id] = in_node
                else:
                    self.open_list.append(node)
                    node.g_score = current_cost
                    node.h_score = self.hami_dist(node)
                    node.parent = current_node
                    h_open_list[node.id] = node
            self.close_list.append(current_node)
            h_close_list[current_node.id] = current_node
            if len(self.open_list) > 0:
                self.open_list = self.open_list[1:]
        return None

    def get_path(self):
        the_list = []
        node = self.calcul()
        if node == None:
            print("No path")
            return the_list
        while node != None:
            the_list.append(node.id)
            node = node.parent
        return the_list

    def gen_nodes(self, current_node):
        node_list = []
        x = current_node.x
        y = current_node.y
        if x - 1 >= 0:
            self.__create_nodes(x - 1, y, node_list)
            if y - 1 >= 0:
                self.__create_nodes(x - 1, y - 1, node_list)
            if y + 1 <= A_Star.edge_limit:
                self.__create_nodes(x - 1, y + 1, node_list)
        if y - 1 >= 0:
            self.__create_nodes(x, y - 1, node_list)
        if y + 1 <= A_Star.edge_limit:
            self.__create_nodes(x, y + 1, node_list)
        if x + 1 <= A_Star.edge_limit:
            self.__create_nodes(x + 1, y, node_list)
            if y - 1 >= 0:
                self.__create_nodes(x + 1, y - 1, node_list)
            if y + 1 <= A_Star.edge_limit:
                self.__create_nodes(x + 1, y + 1, node_list)
        return node_list

    def __create_nodes(self, x, y, node_list):
        node_id = "[%d,%d]" % (x, y)
        # for inode in self.obstacles:
        #     if inode.id == node_id:
        #         return
        if any(x.id == node_id for x in self.obstacles):
            return
        else:
            node_list.append(Node(node_id))

    def dis(self, node1, node2):
        if node1.element[0] == node2.element[0] \
                or node1.element[1] == node2.element[1]:
            return 10
        else:
            return 14


if __name__ == "__main__":
    start = '[1,2]'
    end = '[7,2]'
    obstacles = ['[4,1]', '[4,2]', '[4,3]', '[4,0]']
    a_star = A_Star(obstacles=obstacles, start=start, end=end)
    a_star.get_path()
