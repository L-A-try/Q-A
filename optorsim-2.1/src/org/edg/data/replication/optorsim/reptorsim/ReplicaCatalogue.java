package org.edg.data.replication.optorsim.reptorsim;

import org.edg.data.replication.optorsim.infrastructure.DataFile;

import java.util.HashSet;
import java.util.Hashtable;
import java.util.Set;

/**
 * This class is a catalogue of files available on the Grid. Logical
 * File Names (strings representing a unique file ) are mapped
 * to the physical DataFiles (individual instances or replicas of each
 * file) spread around the Grid using a Hashtable. The keys are the 
 * Logical File Names (string) and the values are Sets of DataFiles.
 * The ReplicaCatalogue is not used directly but is accessed via the
 * ReplicaManager which provides methods to for example copy a file
 * around the Grid or remove a file from the Grid.
 * 这个类是网格上可用的文件目录。合乎逻辑的将映射文件名（表示唯一文件的字符串）
 *到物理数据文件（每个文件的单个实例或副本）*文件）使用哈希表在网格中展开。钥匙是钥匙
 **逻辑文件名（字符串）和值是数据文件集。ReplicaCatalogue不直接使用，而是通过
 **ReplicaManager，提供复制文件的方法或从网格中删除文件。
 * 李昂
 * <p>
 * Copyright (c) 2002 CERN, ITC-irst, PPARC, on behalf of the EU DataGrid.
 * For license conditions see LICENSE file or
 * <a href="http://www.edg.org/license.html">http://www.edg.org/license.html</a>
 * <p>
 * @since JDK1.4
 */ 
class ReplicaCatalogue {
	private Hashtable _catalogue;
	
	protected ReplicaCatalogue() {
		_catalogue=new Hashtable();
	}

	


	
	
	
    /**
     * Add a new DataFile to the catalogue.
     */
	protected synchronized void addFile( DataFile file) {
		System.out.println("--------ReplicaCatalogue---addFile--------------");
		String logicalFileName = file.lfn();
		System.out.println("fileName:"+file.oString());
		if( isStored( file)) {
			System.out.println("RC> ERROR: File "+file+" already registered");
			return; 
		}

		Set fileCollection = getDataFiles( logicalFileName);
		
		if( fileCollection == null) {
			fileCollection = new HashSet();//李昂 还是空的啊  目录里面这个文件没有注册
			_catalogue.put( logicalFileName, fileCollection);
		}
			
		fileCollection.add( file);//之后就存储上了
		System.out.println("rc addfile了看看rc");
		System.out.println(_catalogue.toString());
	}

	/**
	 * Check to see if a particular DataFile is registered.
	 * @param file The file to check
	 * @return whether the file is registered
	 */	
	protected synchronized boolean isStored( DataFile file) {
		String lfn = file.lfn();
		
		if( ! _catalogue.containsKey(lfn))
			return false;
			
		Set replicas = getDataFiles( lfn);
		return replicas.contains( file);
	}

    /**
     * Return the Set of Datafiles associated with the Logical File Name
     * logicalFileName, ie all the replicas of the file named
     * logicalFileName.
     */
	protected synchronized Set getDataFiles(String logicalFileName) {
		return (Set)_catalogue.get(logicalFileName);
	}

    /**
     * Return the Set of Datafiles associated with the Logical File Name
     * logicalFileName as an array.
     */
 	protected synchronized DataFile[] getDataFilesArray(String logicalFileName) {
		System.out.println("--------ReplicaCatalogue---getDataFilesArray--------------");
		Set replicaSet = getDataFiles(logicalFileName);
		/**------------------------------------
		     * @author 李昂
		     * @return 得到文件的存储地点
		**/
		System.out.println(replicaSet);
		if( replicaSet == null)
		    return new DataFile[0];

		DataFile replicaArray[] = new DataFile[replicaSet.size()];
		replicaSet.toArray( replicaArray);
		return replicaArray;
	}

    /**
     * Remove a DataFile from the catalog.
     */
	protected synchronized void removeFile( DataFile file) {
		String logicalFileName = file.lfn();
		Set deletedFile = getDataFiles( logicalFileName);
		
		if (deletedFile.contains(file))
			deletedFile.remove(file);
		else
			System.out.println("RC> ERROR: Cannot delete a file that does not exist!");
	}

}
