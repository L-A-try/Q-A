package org.edg.data.replication.optorsim.optor;

import org.edg.data.replication.optorsim.infrastructure.DataFile;
import org.edg.data.replication.optorsim.infrastructure.GridSite;
import org.edg.data.replication.optorsim.infrastructure.StorageElement;
import org.edg.data.replication.optorsim.reptorsim.ReplicaManager;

import java.util.Iterator;
import java.util.List;

/**
 * This optimiser provides an implementation of getBestFile()
 * which will attempt to perform replication of files to the close Storage
 * Element of the Computing Element calling it (if the file is not already
 * available there). If there is space on the close SE replcation will
 * always suceed. If there is no space the chooseFileToDelete() method
 * of the subclass is called to determine which files should be removed
 * to create space. The implementation of this method should be such that
 * it returns a null value if replication is not to take place, for example
 * if all the files on the local SE are master files or the optimsation
 * algorithm decides it is not worthwhile to replicate.
 * <p>李昂
 *     此优化程序提供了getBestFile（）的实现，它将尝试将文件复制到调用它的计算元素的close Storage元素（如果该文件在那里还不可用）。
 *     如果有空间的话，你的回复总是会成功的。如果没有空间，则调用子类的chooseFileToDelete（）方法来确定应删除哪些文件以创建空间。
 *     如果不进行复制，则此方法的实现应该返回空值，例如，如果本地SE上的所有文件都是主文件，或者OptimstationAlgorithm决定不值得复制。
 * Copyright (c) 2004 CERN, ITC-irst, PPARC, on behalf of the EU DataGrid.
 * For license conditions see LICENSE file or
 * <a href="http://www.edg.org/license.html">http://www.edg.org/license.html</a>
 * <p>
 * @since JDK1.4
 */
abstract public class ReplicatingOptimiser extends SkelOptor {

    public ReplicatingOptimiser( GridSite site) {
	super(site);
    }
    
    /**
     * Always tries to replicate all the files specified by lfns to
     * the calling Computing Element's local Storage Element.
     * Replication will fail if a null is returned by the subclass'
     * chooseFileToDelete method.
     */
    public DataFile[] getBestFile(String[] lfns, 
				  float[] fileFraction) 
    {
    	System.out.println("--------ReplicatingOptimiser---getBestFile--------------");
    	DataFile[] files;
    	
    	files = super.getBestFile( lfns, fileFraction);

		StorageElement closeSE = _site.getCloseSE();
		ReplicaManager rm = ReplicaManager.getInstance();//全局的一个变量
		
		if( closeSE != null) {
			for( int i = 0; i < files.length; i++) {
				/**------------------------------------
				 * @author 李昂
				 * @return
				 **/
//				System.out.println("====+++replicatingoptimiser=====");
//				System.out.println(files[i].toString());

				StorageElement se = files[i].se();

				// skip over any file stored on the local site 李昂 跳过本地站点上存储的任何文件
				if( se.getGridSite() == _site)
					continue;	
				
				DataFile replicatedFile;

				// Check to see if there is a possibility of replication to close SE检查是否有可能复制以关闭SE
				if(!closeSE.isTherePotentialAvailableSpace(files[i]))
					continue;					

				// Loop trying to delete a file on closeSE to make space
				do {
					
					// Attempt to replicate file to close SE.
					replicatedFile = rm.replicateFile( files[i], closeSE);
					
					// If replication worked, store it and move on to next file (for loop)
					if( replicatedFile != null) {
                        files[i].releasePin();
						files[i] = replicatedFile;
						break;
					}
					
					// If replication didn't work, try finding expendable files.如果复制不起作用，请尝试查找可消耗的文件。
					List expendable = chooseFilesToDelete( files[i], closeSE);

					// didn't find one, fall back to remoteIO
					if( expendable == null) {
						break;
					}
					
					for (Iterator it = expendable.iterator(); it.hasNext() ;){
						rm.deleteFile( (DataFile) it.next());
					}

				} while( replicatedFile == null);
				
			} // for
		}
		return files;			
	}
	
    /**
     * How to decide which files to delete in order to make space for DataFile file.
     * All subclasses must implement this using their own optimiser specific algorithms.
     * @param file The file we wish to replicate
     * @param se The SE onto which file is to be replicated
     * @return the files in se to delete, or null if replication isn't to take place
     */
    abstract protected List chooseFilesToDelete( DataFile file, StorageElement se);

}
