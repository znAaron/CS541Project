class TreeNode:
    def __init__(self, key, value, height=1, left=None, right=None):
        self.key = key
        self.value = value
        self.height = height
        self.left = left
        self.right = right


class TreeMap:
    def __init__(self):
        self.root = None

    def put(self, key, value):
        self.root = self._put(self.root, key, value)

    def _put(self, node, key, value):
        if node is None:
            return TreeNode(key, value)

        if key < node.key:
            node.left = self._put(node.left, key, value)
        elif key > node.key:
            node.right = self._put(node.right, key, value)
        else:
            node.value = value
            return node

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        return self._balanced_node(node)

    def _height(self, node):
        if node is None:
            return 0
        return node.height

    def _balanced_node(self, node):
        if self._balance_factor(node) > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            node = self._rotate_right(node)
        elif self._balance_factor(node) < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            node = self._rotate_left(node)

        return node

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    def _rotate_left(self, node):
        new_root = node.right
        node.right = new_root.left
        new_root.left = node

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        new_root.height = 1 + max(self._height(new_root.left), self._height(new_root.right))

        return new_root

    def _rotate_right(self, node):
        new_root = node.left
        node.left = new_root.right
        new_root.right = node

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        new_root.height = 1 + max(self._height(new_root.left), self._height(new_root.right))

        return new_root

    def ceiling(self, key):
        result = self._ceiling(self.root, key)
        if result is None:
            return None
        return result.key, result.value

    def _ceiling(self, node, key):
        if node is None:
            return None

        if key == node.key:
            return node

        if key > node.key:
            return self._ceiling(node.right, key)

        left_ceiling = self._ceiling(node.left, key)
        if left_ceiling is None:
            return node
        else:
            return left_ceiling

    def ceiling_iterator(self, key):
        return self._ceiling_iterator(self.ceiling(key))

    def ceiling_iterator(self, key):
        start_key_value = self.ceiling(key)
        return self._ceiling_iterator(self.root, start_key_value)

    def _ceiling_iterator(self, node, start_key_value):
        if node is None:
            return

        for k, v in self._ceiling_iterator(node.left, start_key_value):
            if k >= start_key_value[0]:
                yield k, v

        yield node.key, node.value

        for k, v in self._ceiling_iterator(node.right, start_key_value):
            yield k, v