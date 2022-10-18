package org.edg.data.replication.optorsim.reptorsim;

import org.edg.data.replication.optorsim.infrastructure.DataFile;
import org.edg.data.replication.optorsim.infrastructure.StorageElement;

import java.util.Date;

/**------------------------------------
     * @author 李昂
     * @return 存储修改后主文件的信息
**/
public class WriteMaiManage  {
    /**------------------------------------
         * @author 李昂
         * @return 存储 主文件站点
    **/
    private StorageElement _se;
    /**------------------------------------
         * @author 李昂
         * @return 存储 文件最后修改时间
    **/
    private Date _timestamp;
    private DataFile dataFile;

    public WriteMaiManage(StorageElement _se, Date _timestamp,DataFile dataFile) {
        this._se = _se;
        this._timestamp = _timestamp;
        this.dataFile=dataFile;
    }

    public DataFile getDataFile() {
        return dataFile;
    }

    public void setDataFile(DataFile dataFile) {
        this.dataFile = dataFile;
    }

    public StorageElement get_se() {
        return _se;
    }

    public void set_se(StorageElement _se) {
        this._se = _se;
    }

    public Date get_timestamp() {
        return _timestamp;
    }

    public void set_timestamp(Date _timestamp) {
        this._timestamp = _timestamp;
    }

    @Override
    public String toString() {
        return "WriteMaiManage{" +
                "_se=" + _se +
                ", _timestamp=" + _timestamp +
                ", dataFile=" + dataFile +
                '}';
    }
}
