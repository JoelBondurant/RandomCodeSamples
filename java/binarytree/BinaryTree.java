package com.analyticobjects.binarytree;

import java.util.LinkedList;
import java.util.Queue;

public class BinaryTree {
	
	private final Node rootNode;
	
	public BinaryTree() {
		this.rootNode = new Node("A");
		this.rootNode.addLeft("B").addLeft("D").addLeft("G").parent().addRight("H");
		this.rootNode.addRight("C").addRight("F");
		this.rootNode.left().addRight("E");
	}
	
	public static void main(String[] args) {
		BinaryTree bt = new BinaryTree();
		bt.traverseBreadthFirst();
	}
	
	public void traverseBreadthFirst() {
		Queue<Node> nodeQueue = new LinkedList<>();
		nodeQueue.add(rootNode);
		Node node;
		while (true) {
			node = nodeQueue.poll();
			if (node == null) {
				break;
			}
			node.printName();
			if (node.hasLeft()) 
				nodeQueue.add(node.left());
			if (node.hasRight())
				nodeQueue.add(node.right());
		}
	}
	
	public class Node {

		private final String name;
		private Node parent;
		private Node left;
		private Node right;

		Node(String name) {
			this.name = name;
		}

		public Node left() {
			return this.left;
		}

		public Node right() {
			return this.right;
		}

		public Node parent() {
			return this.parent;
		}

		public boolean hasLeft() {
			return this.left != null;
		}

		public boolean hasRight() {
			return this.right != null;
		}

		public Node addLeft(String name) {
			this.left = new Node(name);
			this.left.parent = this;
			return this.left;
		}

		public Node addRight(String name){
			this.right = new Node(name);
			this.right.parent = this;
			return this.right;
		}

		public void printName() {
			System.out.println(name);
		}

	}
	
}
