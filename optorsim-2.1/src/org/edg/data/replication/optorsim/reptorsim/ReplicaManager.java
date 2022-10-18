package org.edg.data.replication.optorsim.reptorsim;

import org.edg.data.replication.optorsim.infrastructure.DataFile;
import org.edg.data.replication.optorsim.infrastructure.GridContainer;
import org.edg.data.replication.optorsim.infrastructure.StorageElement;

/**
 * The ReplicaManager provides file manipulation methods and interfaces
 * between the Computing Elements and optimisers and the low level
 * Grid infrastructure. It also acts as a wrapper class for the
 * ReplicaCatalogue, so that any changes to it must go through the
 * methods of this class.
 * <p>
 * Copyright (c) 2002 CERN, ITC-irst, PPARC, on behalf of the EU DataGrid.
 * For license conditions see LICENSE file or
 * <a href="http://www.edg.org/license.html">http://www.edg.org/license.html</a>
 * <p>
 * @since JDK1.4
 */
public class ReplicaManager  {

    /**
     * STATIC singleton handler
     */

    private static ReplicaManager _replicaManagerInstance = null;

    /** Returns the (singleton) instance of the ReplicaManager.*/ 
    public static ReplicaManager getInstance() {
		if( _replicaManagerInstance == null) 
	    	_replicaManagerInstance = new ReplicaManager();

		return _replicaManagerInstance;
    }


    private ReplicaCatalogue _rc;
    private MaiCatalogue _mc;
    private final int ALL_OF_FILE=1;

    private ReplicaManager() {
		_rc = new ReplicaCatalogue();
		_mc = new MaiCatalogue();
    }

    /**
     * Register an entry in the ReplicaCatalogue.
     */
    public void registerEntry( DataFile file) {
        System.out.println("--------ReplicaManager---registerEntry--------------");
		_rc.addFile( file);
		/**------------------------------------
		     * @author 李昂
		     * @return 创建文件时用
		**/
        System.out.println("rm registerEntry----------------------创建文件维护主列表");
        _mc.addFile(file);

    }//李昂 注册文件目录

    /**------------------------------------
         * @author 李昂
         * @return 缓存后 只注册目录的方法
    **/
    public void rEn(DataFile file){
        System.out.println("缓存注册目录");
        _rc.addFile(file);
    }

    public WriteMaiManage get_mc_thing(String fileName) {
        return _mc.getDataFiles(fileName);
    }

    /**
     * Remove an entry from the ReplicaCatalogue.
     */
    public void unregisterEntry( DataFile file) {

		_rc.removeFile( file);
		/**------------------------------------
		     * @author 李昂
		     * @return 删除文件
		**/
		_mc.removeFile(file);
    }

    /**
     * Copy a file to a SE, and register it in the Replica Catalogue.
     * @param source The file we wish to replicate
     * @param toSE  The destination SE
     * @return The new replica if successful, null otherwise
     */
    //复制文件 目录里面增添
    //选择在哪复制也得看一下
    /**------------------------------------
         * @author 李昂
         * @return 复制文件+目录增加  主文件目录不添加
    **/
    public DataFile replicateFile( DataFile source, StorageElement toSE) {
        System.out.println("rm replicateFile----------------------");
		GridContainer gc = GridContainer.getInstance();
		DataFile newFile = gc.replicate( source, toSE);

		if( newFile != null)
			_rc.addFile( newFile);
//        System.out.println("rm replicateFile----------------------创建文件维护主列表");
//        _mc.addFile(newFile);
		return newFile;
    }

    /**没用到，复制文件，目录里面不注册 不大对啊  是副本 就得注册
     * Copy a file to a SE, but do not register it in the 
     * Replica Catalogue. The file is "cached" in the destination SE.
     * @param source The file we wish to copy
     * @param toSE  The destination SE
     */

    public DataFile reCopy( DataFile source, StorageElement toSE) {
        System.out.println("rm reCopy----------------------");
        GridContainer gc = GridContainer.getInstance();
        DataFile newFile = gc.replicate( source, toSE);
//        System.out.println("rm reCopy----------------------创建文件维护主列表");
//        _mc.addFile(newFile);
        return newFile;
    }

    public void copyFile( DataFile source,  StorageElement toSE) {
		GridContainer gc = GridContainer.getInstance();			
		gc.copy( source, toSE.getGridSite(), ALL_OF_FILE);
    }
    /**------------------------------------
         * @author 李昂
         * @return 删除没有修改的文件
    **/
    public void delete( DataFile file) {
        StorageElement se = file.se();
        se.removeFile(file);
    }

    /**
     * Delete a DataFile from the Grid, physically deleting it
     * from the Storage Element and unregistering it with the 
     * Replica Catalogue.
     */
    public void deleteFile( DataFile file) {
		_rc.removeFile( file);
	
		StorageElement se = file.se();
		se.removeFile(file);
    }

    /**
     * Returns an array of all the replicas of filename on the Grid.
     * @return Array of DataFiles which are replicas of filename.
     */
    public DataFile[] listReplicas(String filename) {
        System.out.println("--------ReplicaManager---listReplicas--------------");
		return _rc.getDataFilesArray(filename);
    }



}




