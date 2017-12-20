package com;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.HashMap;

public class Tools {
	
	/**
	 * 遍历前缀树查询后的子节点，将子节点中所有能组成完整词项的结果添加到res数组中
	 * @param cur	查询操作得到Trie树的一个节点
	 * @param tmp	临时字符串，用于拼接生成完整结果，一般是查询词Unicode编码
	 * @param res	查询结果存储数组，该结果仍然是Unicode编码
	 */
	public static void iterator(Trie cur, String tmp, ArrayList<String> res)
	{
		if(cur==null)
			return;
		tmp += cur.value;
		ArrayList<Integer> index_list = cur.index;
		if(cur.isleaf)
		{
			res.add(new String(tmp));
		}
		if (index_list.size()==0)
			return;
		for(int i=0; i < index_list.size(); i++)
		{
			int index = index_list.get(i).intValue();
			Trie curNode = cur.children[index];
			iterator(curNode, tmp, res);
		}
	}
	
	/**
	 * 将词项的轮排插入前缀树中，其对应的映射关系表存储在map中
	 * 映射关系为Unicode -> index, 如 '\\u4e2d\\u24' -> '中'
	 * @param root  Trie树的根节点
	 * @param voc	词项
	 * @param map	轮排到词项的映射字典
	 */
	public static void importVoc(Trie root, String voc, HashMap<String, String> map)
	{
		
		String ori = voc;
		voc += "$";
		int length = voc.length();
		String prefix,postfix,temp;
		for (int i = 0; i < length; i++)
		{
			prefix = voc.substring(0,i);
			postfix = voc.substring(i);
			temp = postfix + prefix;
			map.put(string2Unicode(temp), ori);
			try {
				root.insert(string2Unicode(temp));
			} catch (CharNotAvailable e) {
				e.printStackTrace();
			}
		}
	}
	
	/**
	 * 将前缀树对象序列化处理，导入词项时可以减少耗时，提高效率
	 * @param root 需要被序列化的对象，对象类型为Trie
	 * @param pathname 对象被存储的文件名
	 */
	public static void serializeTrie(Trie root,String pathname)
	{
		try {
			ObjectOutputStream oo = new ObjectOutputStream(
					new FileOutputStream(new File(pathname)));
			oo.writeObject(root);
			System.out.println("序列化成功");
			oo.close();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	/**
	 * 将序列化对象还原
	 * @param pathname
	 * @return
	 */
	public static Trie deserializeTrie(String pathname)
	{
		Trie root = null;
		try {
			ObjectInputStream obj_input_stream = new ObjectInputStream(
					new FileInputStream(new File(pathname)));
			root = (Trie)obj_input_stream.readObject();
			obj_input_stream.close();
		}  catch (Exception e) {
			e.printStackTrace();
		}
		return root;
		
	}
	
	/**
	 * 将文件中的词项加载到前缀树中
	 * @param fileName 文件名
	 * @param root 前缀树根节点
	 * @param map 存储映射关系，轮排到词项的映射关系
	 */
	public static void loadTerm(String fileName,Trie root, HashMap<String, String> map)
	{
		
		try {
			FileInputStream fin = new FileInputStream(new File(fileName));
			BufferedReader br = new BufferedReader(new InputStreamReader(fin,"utf-8"));
			String lineTxt = null;
			while((lineTxt=br.readLine())!=null)
			{
				importVoc(root, lineTxt, map);
			}
			fin.close();
			root.setMap(map);
		} catch (Exception e) {
			e.printStackTrace();
		}
		
	}
	
	/**
	 * 通配符前缀匹配搜索，搜索结果存储于res数组中
	 * @param target 搜索词项
	 * @param root 前缀树根节点
	 * @param res 结果集
	 */
	public static void search(String target, Trie root, ArrayList<String> res)
	{
		Trie tree = root.search(string2Unicode(target));
		if (tree!=null)
		{
			Trie cur = tree;
			if (cur.isleaf)
			{
				res.add(root.getMap().get(string2Unicode(target)));
			}
			ArrayList<String> str_res = new ArrayList<String>();
			String tmp_str = "";
			for(int i =0; i<cur.index.size();i++)
			{
				Trie node = cur.children[cur.index.get(i).intValue()];
				Tools.iterator(node, tmp_str, str_res);
			}
			
			for(int i =0; i < str_res.size();i++)
			{
				String result = string2Unicode(target)+str_res.get(i);
				res.add(root.getMap().get(result));
			}
		}
		
	}
	
	/**
	 * 将字符串转化成Unicode编码
	 * @param string 
	 * @return
	 */
	public static String string2Unicode(String string) {  
	    StringBuffer unicode = new StringBuffer();  
	    for (int i = 0; i < string.length(); i++) {  
	        char c = string.charAt(i);  
	        unicode.append("\\u" + Integer.toHexString(c));  
	    }  
	    return unicode.toString();  
	}  

	public static String unicode2String(String unicode) {  
		   
	    StringBuffer string = new StringBuffer();  
	    String[] hex = unicode.split("\\\\u");  
	    for (int i = 1; i < hex.length; i++) {  
	        int data = Integer.parseInt(hex[i], 16);  
	        string.append((char) data);  
	    }  
	    return string.toString();  
	} 
}
