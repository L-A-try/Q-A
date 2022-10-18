package org.edg.data.replication.optorsim.optor;

import org.edg.data.replication.optorsim.infrastructure.ComputingElement;
import org.edg.data.replication.optorsim.infrastructure.DataFile;
import org.edg.data.replication.optorsim.infrastructure.GridSite;
import org.edg.data.replication.optorsim.infrastructure.StorageElement;
import org.edg.data.replication.optorsim.reptorsim.NetworkClient;
import org.edg.data.replication.optorsim.reptorsim.NetworkCost;
import org.edg.data.replication.optorsim.reptorsim.ReplicaManager;
import org.edg.data.replication.optorsim.reptorsim.WriteMaiManage;

import java.util.Date;
import java.util.Random;

/**
 * This class is the basic implementation of the {@link Optimisable}
 * interface. It provides the basic operations required for all the 
 * optimisation classes and simple versions of the two most important
 * methods: getAccessCost() and getBestFile(). getAccessCost()
 * calculates the expected cost to access the specified files from the
 * specified ComputingElement using network information to work out the
 * best replica to use for each file in terms of network latencies.
 * <p>
 * getBestFile() uses the same network information to return, for each
 * file given, the replica that can be accessed from the Computing Element
 * calling the method in the quickest time. This class should not be
 * instantiated itself, but subclasses should be used which overload
 * the methods as required.
 * <p>
 * Copyright (c) 2004 CERN, ITC-irst, PPARC, on behalf of the EU DataGrid.
 * For license conditions see LICENSE file or
 * <a href="http://www.edg.org/license.html">http://www.edg.org/license.html</a>
 * <p>
 * @since JDK1.4
 */
public class SkelOptor implements Optimisable {

    protected GridSite _site;
    protected NetworkClient _networkClient;

    /**
     * This constructor should only be called from SkelOptor
     * subclasses
     */
    protected SkelOptor( GridSite site) {

		_site = site;
		_networkClient =  new NetworkClient();
    }

    // TODO: factor out jbook from optimisers so the same constructor
    // can be used from CEs and the RB.
    protected SkelOptor() {
		_networkClient = new NetworkClient();
    }
 
    /**
     * A "standard" implementation of getBestFile. It simply looks at
     * the Replica Catalogue and current network status and returns the
     * replicas that will take the shortest time to access.
	 * 它只是看副本目录和当前网络状态，并返需要最短时间访问的复制副本
	 * --只是找到最好的 存储到列表里面 并不进行操作
	 * 找到最好地点存储，响应最快的地方进行存储  以及更新（更新上时间戳哦，存储上时间戳）
     */
    public DataFile[] getBestFile( String[] lfns, 
							      float[] fileFraction) {
    	System.out.println("--------SkelOptor---getBestFile--------------");
		DataFile files[] = new DataFile[lfns.length];
		DataFile replicas[];
		int i,j;
        NetworkCost minNC = null;
        ReplicaManager rm = ReplicaManager.getInstance();
		
		// For each requested LFN
		for(i=0;i<lfns.length;i++) {
		    
		    do {
				replicas = rm.listReplicas(lfns[i]);//这个文件的所有存储地点
				//得到 主文件目录
				WriteMaiManage mc_thing = rm.get_mc_thing(lfns[i]);
				// Find the cheapest file:
				for(j=0;j<replicas.length;j++) {
					/**------------------------------------
					 * @author 李昂
					 * @return
					 **/
					System.out.println("p==============="+j);
					System.out.println(replicas[j].toString());

					replicas[j].addPin(); // pin the file
					StorageElement remoteSE = replicas[j].se();
					//这个文件的时间
					Date lastChangeTime = replicas[j].getLastChangeTime();
					//If file has been deleted since listReplicas
					if( remoteSE==null){
						continue ;
					}
					    
					GridSite remoteSite = remoteSE.getGridSite();//得到存储文件的这个站点

					// If this is the same site, always use it.							    
					if( remoteSite == _site) {
						/**------------------------------------
						     * @author 李昂
						     * @return 看看有的这个文件 是不是主文件 是-用 不是-更新
						**/


						if((long)lastChangeTime.getTime()<(long)mc_thing.get_timestamp().getTime()){
							//跟主站点更新 不注册-copy   已经有了 要先删掉原来的  吗？？
							rm.delete(replicas[j]);
							System.out.println("删除了111111111111111111111");
							System.out.println("lllp");
							replicas[j]=rm.reCopy(mc_thing.getDataFile(),remoteSE);
						}



						if(files[i]!=null)
							files[i].releasePin() ; // unpin previously selected file取消固定进行修改
						System.out.println("还有吗32222222222222222");
						System.out.println(replicas[j]);

						files[i] = replicas[j];//原来有这个文件
						break;
					}
					//看损失去--李昂
					int transferSize = (int) (replicas[j].size() * fileFraction[i]);
					NetworkCost nc = _networkClient.getNetworkCosts( remoteSite, _site,  transferSize);
						
					if( (j == 0) || (nc.getCost() <= minNC.getCost())) {
						
						if( (j != 0) && (nc.getCost() == minNC.getCost())) {
							//消耗的值一样，随机选择 哪个站点=-李昂---后期可以不让随机，而站点最好的一个
							Random random = new Random();
							if( random.nextFloat() < 0.5) {
								minNC = nc;
								/**------------------------------------
								     * @author 李昂
								     * @return 这个时间 小余 就需要复制
								**/
								if((long)lastChangeTime.getTime()<(long)mc_thing.get_timestamp().getTime()){
									//跟主站点更新 不注册-copy   已经有了 要先删掉原来的  吗？？
									rm.delete(replicas[j]);
									System.out.println("llln");
									System.out.println("删除了111111111111111111111");
									replicas[j]=rm.reCopy(mc_thing.getDataFile(),remoteSE);
								}


								if(files[i]!=null)
								 	files[i].releasePin() ;
								 //每一个 都应该看时间戳
								 files[i] = replicas[j];
							}
						}
						else {
							minNC = nc;
							if((long)lastChangeTime.getTime()<(long)mc_thing.get_timestamp().getTime()){
								//跟主站点更新 不注册-copy   已经有了 要先删掉原来的  吗？？
								//还是一个东西嘛
                                replicas[j].releasePin() ;
								System.out.println("删除了111111111111111111111");
								replicas[j]=rm.reCopy(mc_thing.getDataFile(),remoteSE);
								System.out.println(replicas[j]);

							}

							if(files[i]!=null)
								files[i].releasePin() ; // unpin previously selected file
							        
							files[i] = replicas[j];
						}
					}
					else { // replicas[j] not a good candidate,
					replicas[j].releasePin(); // unpin it
					}
				}
			} while( files[i] == null);
		}    
		return files;
	}

    /**
     * Calculate aggregated network costs for a single computing element.
     * Uses network costs and the Replica Catalog to find the best replica
     * of each file and sums the access costs.y要你何用啊，最后还要找每个文件副本 看代价
     */
    public float getAccessCost(String[] lfns,
				ComputingElement ce,
				float[] fileFraction) {
    	System.out.println("--------SkelOptor---getAccessCost--------------");
		float aggregatedCost = 0;
		ReplicaManager rm = ReplicaManager.getInstance();
		float minCost = 0;

		GridSite ceGridSite = ce.getSite();

		for(int i=0; i<lfns.length; i++) {

	    	DataFile files[] = rm.listReplicas(lfns[i]);
	    	boolean minCostUninitialised = true;

	    	for(int j=0; j<files.length; j++) {

				if( files[j] == null)
		    		continue;
		    	
				StorageElement remoteSE = files[j].se();

				//看有没删除副本
				if( remoteSE == null)
				    continue;

				GridSite seGridSite = remoteSE.getGridSite();
		    
				// 判断文件是否在本地站点，是的话不在找副本
				if( ceGridSite == seGridSite) {
		    		minCostUninitialised = false;
		    		minCost = 0;
			    	break;
				}

				NetworkCost nc = _networkClient.getNetworkCosts( seGridSite, ceGridSite, 
								     														files[j].size());

				if( (nc.getCost() < minCost) || minCostUninitialised) {
			    	minCostUninitialised = false;
			    	minCost = nc.getCost();
				}
		    }

		    if( minCostUninitialised) {
				System.out.println( "optor> didn't find any replica for LFN "+lfns[i]);
				continue;
		    }

		    aggregatedCost += minCost;
		}

		return aggregatedCost;
    }


    public void initFilePrefetch(String[]  lfn,
				 ComputingElement ce)
    {
		System.out.println("initFilePrefetch");
    }

    
    public void cancelFilePrefetch(String[] lfn,
				   ComputingElement CE)
    {
		System.out.println("cancelFilePrefetch");
    }

}







