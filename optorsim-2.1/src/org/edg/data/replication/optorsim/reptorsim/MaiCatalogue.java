package org.edg.data.replication.optorsim.reptorsim;

import org.edg.data.replication.optorsim.infrastructure.DataFile;
import org.edg.data.replication.optorsim.infrastructure.StorageElement;

import java.util.Date;
import java.util.Hashtable;

/**------------------------------------
     * @author 李昂
     * @return 操作主文件的信息
**/
public class MaiCatalogue {

    private Hashtable _catalogue;
    /**------------------------------------
         * @author 李昂
         * @return 初始化
    **/
    protected MaiCatalogue() {
        _catalogue=new Hashtable();
    }
    /**------------------------------------
         * @author 李昂
         * @return 添加主文件到列表里面（写操作的时候才对其访问- 创建文件 写文件)
    **/
    protected synchronized void addFile( DataFile file) {
        System.out.println("--------MaiCatalogue---addFile--------------");
        //得到文件的write时间  与主文件对应的查看，谁大写谁
        String logicalFileName = file.lfn();
        //写文件的时候这个采用
//        System.out.println(file.oString());
        Date lastChangeTime = file.getLastChangeTime();//修改时间
        StorageElement se = file.se();//文件站点

        //此文件 列表中存在否
          //不存在 直接更新 over
        if(!isStored( file)) {
            System.out.println("不存在 要更新主文件目录");
            WriteMaiManage writeMaiManage= new WriteMaiManage(se,lastChangeTime,file);
            _catalogue.put( logicalFileName, writeMaiManage);
            System.out.println(_catalogue.toString());
            return;
        }
          //存在 比较 变换
        WriteMaiManage dataFiles = getDataFiles(logicalFileName);
        long cunTime=dataFiles.get_timestamp().getTime();
        long comeTime=lastChangeTime.getTime();

        if(comeTime>cunTime){
            dataFiles.set_se(se);
            dataFiles.set_timestamp(lastChangeTime);
            dataFiles.setDataFile(file);
            _catalogue.put(logicalFileName,dataFiles);
        }

        System.out.println(_catalogue.toString());
        return;
    }

    
    /**------------------------------------
         * @author 李昂
         * @return 看看 时间列表里面有没有那个文件
    **/
    protected synchronized boolean isStored( DataFile file) {
        String lfn = file.lfn();

        if( ! _catalogue.containsKey(lfn))
            return false;
        //存
        return true;
    }

    /**------------------------------------
         * @author 李昂
         * @return 返回文件 主副本信息 WriteMaiManage
    **/
    protected synchronized WriteMaiManage getDataFiles(String logicalFileName) {
        return (WriteMaiManage) _catalogue.get(logicalFileName);
    }


    /**
     * Remove a DataFile from the catalog.
     */
    protected synchronized void removeFile( DataFile file) {
        String logicalFileName = file.lfn();

        if (isStored(file))
            _catalogue.remove(file);
        else
            System.out.println("RC> ERROR: Cannot delete a file that does not exist!");
    }



}
