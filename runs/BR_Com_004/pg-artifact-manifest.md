# PG artifact manifest BR_Com_004

Danh sách file PG và build/lint config đã review G1. Path tuyệt đối hoặc tương đối từ task.
Role ghi rõ production-code hoặc build-config.
Không yêu cầu UT code tại G1. Danh sách PG/UT cuối nằm trong artifact-manifest.md ở S5.
File thiếu chặn kiểm tra. User tự commit; SHA ghi nếu có.

Code commit: không bắt buộc (user tự commit trên branch `bd-to-pg`).

## Files

| ID | Path | Role |
|---|---|---|
| F-01 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasDomain\Models\Room.cs | production-code (new) |
| F-02 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasDomain\Models\Tablet.cs | production-code (new) |
| F-03 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasDomain\Models\CandidateRoom.cs | production-code (new) |
| F-04 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasDomain\Repositories\IRoomRepository.cs | production-code (new) |
| F-05 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasDomain\Repositories\ITabletRepository.cs | production-code (new) |
| F-06 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasInfrastructure\RasDbContext.cs | production-code (modified, shared) |
| F-07 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasInfrastructure\EntityConfigurations\RoomEntityTypeConfiguration.cs | production-code (new) |
| F-08 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasInfrastructure\EntityConfigurations\TabletEntityTypeConfiguration.cs | production-code (new) |
| F-09 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasInfrastructure\EntityConfigurations\CandidateRoomEntityTypeConfiguration.cs | production-code (new) |
| F-10 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasInfrastructure\Repositories\RoomRepository.cs | production-code (new) |
| F-11 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasInfrastructure\Repositories\TabletRepository.cs | production-code (new) |
| F-12 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasUseCase\ViewModels\TabletInfoModels.cs | production-code (new) |
| F-13 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasUseCase\Services\ITabletInfoService.cs | production-code (new) |
| F-14 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasUseCase\Services\TabletInfoService.cs | production-code (new) |
| F-15 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi\ViewModels\TabletInfoRequests.cs | production-code (new) |
| F-16 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi\Controllers\TabletInfoController.cs | production-code (new) |
| F-17 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi\Controllers\RoomsController.cs | production-code (new) |
| F-18 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi\Startup.cs | production-code (modified, shared: DI) |
| F-19 | D:\Serio-AI\serio-ras\ras-system\src\BuildingBlocks\Common\Util\Resources\Messages.resx | production-code (modified, shared: message E_BRCOM004_001) |
| F-20 | D:\Serio-AI\serio-ras\ras-web\src\app\features\tablet-registration\components\tablet-registration.component.ts | production-code (new) |
| F-21 | D:\Serio-AI\serio-ras\ras-web\src\app\features\tablet-registration\components\tablet-registration.component.html | production-code (new) |
| F-22 | D:\Serio-AI\serio-ras\ras-web\src\app\features\tablet-registration\components\tablet-registration.component.css | production-code (new) |
| F-23 | D:\Serio-AI\serio-ras\ras-web\src\app\features\tablet-registration\services\tablet-registration.service.ts | production-code (new) |
| F-24 | D:\Serio-AI\serio-ras\ras-web\src\app\features\tablet-registration\interfaces\tablet-info.interface.ts | production-code (new) |
| F-25 | D:\Serio-AI\serio-ras\ras-web\src\app\features\room-search-mock\components\room-search-mock.component.ts | production-code (new, mock BR_Com_003) |
| F-26 | D:\Serio-AI\serio-ras\ras-web\src\app\features\room-search-mock\components\room-search-mock.component.html | production-code (new, mock BR_Com_003) |
| F-27 | D:\Serio-AI\serio-ras\ras-web\src\app\features\room-search-mock\components\room-search-mock.component.css | production-code (new, mock BR_Com_003) |
| F-28 | D:\Serio-AI\serio-ras\ras-web\src\app\features\room-search-mock\interfaces\room-search.interface.ts | production-code (new, mock BR_Com_003 contract) |
| F-29 | D:\Serio-AI\serio-ras\ras-web\src\app\features\error-mock\components\error-mock.component.ts | production-code (new, mock BR_Com_005) |
| F-30 | D:\Serio-AI\serio-ras\ras-web\src\app\features\error-mock\components\error-mock.component.html | production-code (new, mock BR_Com_005) |
| F-31 | D:\Serio-AI\serio-ras\ras-web\src\app\features\error-mock\components\error-mock.component.css | production-code (new, mock BR_Com_005) |
| F-32 | D:\Serio-AI\serio-ras\ras-web\src\app\app.routes.ts | production-code (modified, shared: routes BRCom004, error/:statusCode) |
| F-33 | D:\Serio-AI\serio-ras\ras-web\src\app\shared\guards\admin.guard.ts | production-code (modified, shared: redirect → /error/403) |
| F-34 | D:\Serio-AI\serio-ras\ras-web\src\app\shared\services\api-error-handler.service.ts | production-code (modified, shared: redirect → /error/{status}) |
| F-35 | D:\Serio-AI\serio-ras\ras-web\src\assets\i18n\ja.json | production-code (modified, shared: i18n keys) |
| F-36 | D:\Serio-AI\serio-ras\ras-system\src\Services\Ras\RasApi\RasApi.csproj | build-config (không sửa; lệnh build) |
| F-37 | D:\Serio-AI\serio-ras\ras-web\angular.json | build-config (không sửa; budget production có sẵn đang vượt) |
