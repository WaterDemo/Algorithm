package com;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;

public class Trie implements Serializable{
	
	private HashMap<String, String> map;
	/**
	 *  serialized id
	 */
	private static final long serialVersionUID = 5809782578272943999L;
	char value; // 前缀树的节点值
	boolean isleaf; // 是否可以作为一个叶子节点
	Trie currentNode; // 搜索时，如果搜索到结果，保存当头节点
	ArrayList<Integer> index; // 前缀树的叶子节点的索引，当前节点的非空子节点的快速索引
	Trie children[]; // 当前节点的子节点
	
	public Trie(char c)
	{
		this.value = c;
		this.children = new Trie[18];
		this.index = new ArrayList<Integer>();
		this.isleaf = false;
		this.currentNode = null;
	}
	
	// 将节点插入前缀树中
	public boolean insert(String str) throws CharNotAvailable
	{
		if ( str.length()==0 || str==null )
			return false;
		int index;
		char [] chrs = str.toCharArray();
		Trie cur = this;
		for (char c : chrs) {
			index = Constant.CODE.indexOf(c);
			if(index==-1)
				throw new CharNotAvailable("输入字符不符合unicode编码");
			if (cur.children[index]==null){
				cur.children[index] = new Trie(c);
				cur.index.add(new Integer(index));
			}
			cur = cur.children[index];
		}
		cur.isleaf = true;
		return true;
	}
	
	// 在前缀树中搜索，如果存在则返回当前节点，否则返回空
	public Trie search(String str)
	{
		if (str.length()==0||str==null)
			return null;
		char [] chrs = str.toCharArray();
		Trie cur = this;
		int index;
		for (char c : chrs) {
			index = Constant.CODE.indexOf(c);
			cur = cur.children[index];
			if (cur==null)
				return null;	
		}
		return cur;	
	}
	
	// 此处的设计其实是有违背耦合性原则的，map的管理应该不属于前缀树
	// 这是为了达到序列化的实现，保证轮排映射表的伴随存在
	public  void setMap(HashMap<String, String> map)
	{
		this.map = map;
	}
	
	public HashMap<String, String> getMap()
	{
		return this.map;
	}
}
