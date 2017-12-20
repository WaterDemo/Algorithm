package com;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import javax.swing.InputMap;

public class Test {
	
	public static void main(String [] args)
	{
		Trie root = new Trie('#');
		String voc_file = "voc.txt";
		String seriableObjectFile = "trie.obj";
		// map 存储轮排到词项的映射
		HashMap<String, String> map = new HashMap<String, String>();
		String target = "道$";
		Tools.loadTerm(voc_file, root, map);
		
		// 此处可以将前缀树对象序列化存储
		// Tools.serializeTrie(root, seriableObjectFile);
		
		// 反序列化还原前缀树对象
		// root = Tools.deserializeTrie(seriableObjectFile);
		
		ArrayList<String> res = new ArrayList<String>();
		Tools.search(target, root, res);
		for (int i = 0; i < res.size(); i++)
		{
			System.out.println(res.get(i));
		}
		res.clear();
		target = "有$";
		Tools.search(target, root, res);
		for (int i = 0; i < res.size(); i++)
		{
			System.out.println(res.get(i));
		}		
	}
	
}
